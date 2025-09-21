import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

MONEY = dict(max_digits=12, decimal_places=2)

class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class Meta:
        abstract = True

# --- Roles & User Profile ---
ROLES = [
    ('DIRECTOR', 'Director'),
    ('HEAD', 'Head Teacher'),
    ('DEPUTY', 'Deputy Head'),
    ('CASHIER', 'Cashier'),
]

class UserProfile(UUIDModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=12, choices=ROLES, null=True, blank=True)
    def __str__(self):
        return f"{self.user.username} ({self.role or 'UNASSIGNED'})"

class ClassLevel(UUIDModel):
    SECTION = [
        ('ECDE', 'ECDE'),
        ('LOWER', 'Lower Primary'),
        ('UPPER', 'Upper Primary'),
        ('JUNIOR', 'Junior Secondary'),
    ]
    section = models.CharField(max_length=10, choices=SECTION)
    name = models.CharField(max_length=64)
    order = models.PositiveSmallIntegerField(help_text='Ordering within section')
    class Meta:
        unique_together = ('section', 'name')
        ordering = ['section', 'order']
    def __str__(self): return f"{self.get_section_display()} - {self.name}"

class AcademicYear(UUIDModel):
    name = models.CharField(max_length=9, unique=True)  # e.g. "2025"
    class Meta: ordering = ['-name']
    def __str__(self): return self.name

class Term(UUIDModel):
    number = models.PositiveSmallIntegerField(choices=[(1, 'Term 1'), (2, 'Term 2'), (3, 'Term 3')])
    year = models.ForeignKey('AcademicYear', on_delete=models.CASCADE, related_name='terms')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    class Meta:
        unique_together = ('year', 'number')
        ordering = ['year__name', 'number']
    def __str__(self): return f"{self.year.name} T{self.number}"

class Student(UUIDModel):
    BOARDING = [('DAY','Day'), ('BOARDING','Boarding')]
    STATUS = [('ACTIVE','Active'), ('TRANSFERRED','Transferred'), ('ALUMNI','Alumni')]

    admission_no = models.CharField(max_length=20, unique=True, db_index=True)
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64)
    dob = models.DateField(null=True, blank=True)
    birth_cert_no = models.CharField(max_length=64, blank=True)
    upi = models.CharField(max_length=64, blank=True)

    father_name = models.CharField(max_length=128, blank=True)
    mother_name = models.CharField(max_length=128, blank=True)
    guardian_name = models.CharField(max_length=128, blank=True)
    guardian_relationship = models.CharField(max_length=64, blank=True)

    contact1 = models.CharField(max_length=64, blank=True)
    residence = models.TextField(blank=True)

    year_enrolled = models.ForeignKey('AcademicYear', on_delete=models.PROTECT, related_name='enrolled_students', null=True, blank=True)
    term_enrolled = models.ForeignKey('Term', on_delete=models.PROTECT, related_name='enrolled_students', null=True, blank=True)
    enrollment_class = models.ForeignKey('ClassLevel', on_delete=models.PROTECT, related_name='enrolled_students', null=True, blank=True)

    boarding_status = models.CharField(max_length=10, choices=BOARDING, default='DAY')
    status = models.CharField(max_length=12, choices=STATUS, default='ACTIVE')

    class Meta: ordering = ['last_name', 'first_name']
    def __str__(self): return f"{self.admission_no} - {self.last_name}, {self.first_name}"

class FeeStructure(UUIDModel):
    BOARDING = Student.BOARDING
    term = models.ForeignKey('Term', on_delete=models.CASCADE, related_name='fee_structures')
    class_level = models.ForeignKey('ClassLevel', on_delete=models.PROTECT, related_name='fee_structures')
    boarding_status = models.CharField(max_length=10, choices=BOARDING)
    amount_kes = models.DecimalField(**MONEY, validators=[MinValueValidator(0)])
    class Meta:
        unique_together = ('term', 'class_level', 'boarding_status')
    def __str__(self): return f"{self.term} {self.class_level.name} {self.boarding_status}: {self.amount_kes}"

class LedgerEntry(UUIDModel):
    ENTRY_TYPE = [('INVOICE','Invoice'), ('PAYMENT','Payment'), ('REVERSAL','Reversal')]
    SOURCE = [('SYSTEM','System'), ('CASH','Cash'), ('BANK_CSV','Bank CSV'), ('MPESA_CSV','M-Pesa CSV'), ('MANUAL_CORRECTION','Manual Correction')]
    MODE = [('CASH','Cash'), ('MPESA','M-Pesa'), ('BANK','Bank')]

    student = models.ForeignKey('Student', on_delete=models.PROTECT, related_name='ledger_entries')
    term = models.ForeignKey('Term', on_delete=models.PROTECT, related_name='ledger_entries')
    date = models.DateField()
    entry_type = models.CharField(max_length=12, choices=ENTRY_TYPE)
    source = models.CharField(max_length=24, choices=SOURCE)
    mode = models.CharField(max_length=10, choices=MODE, null=True, blank=True)
    amount_kes = models.DecimalField(**MONEY)  # positive for INVOICE/PAYMENT; negative for REVERSAL
    reference = models.CharField(max_length=64, blank=True)
    memo = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_entries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        indexes = [models.Index(fields=['student','term']), models.Index(fields=['date'])]
        ordering = ['-date','-created_at']
    def __str__(self): return f"{self.entry_type} {self.amount_kes} {self.student.admission_no} {self.term}"

class Payment(UUIDModel):
    MODE = LedgerEntry.MODE
    student = models.ForeignKey('Student', on_delete=models.PROTECT, related_name='payments')
    term = models.ForeignKey('Term', on_delete=models.PROTECT, related_name='payments')
    date = models.DateField()
    mode = models.CharField(max_length=10, choices=MODE)
    amount_kes = models.DecimalField(**MONEY, validators=[MinValueValidator(0)])
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_payments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edit_count_today = models.PositiveSmallIntegerField(default=0)
    reference = models.CharField(max_length=64, blank=True)
    class Meta:
        indexes = [models.Index(fields=['student','term','date'])]
    def __str__(self): return f"{self.date} {self.mode} {self.amount_kes} {self.student.admission_no}"

class PaymentEditLog(UUIDModel):
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, related_name='edit_logs')
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    edited_at = models.DateTimeField(auto_now_add=True)
    change_summary = models.JSONField(null=True, blank=True)

class ImportBatch(UUIDModel):
    CHANNEL = [('BANK','Bank'), ('MPESA','M-Pesa')]
    STATUS = [('PENDING','Pending'), ('PROCESSED','Processed'), ('PARTIAL','Partial'), ('FAILED','Failed')]
    channel = models.CharField(max_length=10, choices=CHANNEL)
    filename = models.CharField(max_length=200)
    imported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    imported_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS, default='PENDING')

class ImportRow(UUIDModel):
    batch = models.ForeignKey('ImportBatch', on_delete=models.CASCADE, related_name='rows')
    date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(**MONEY, null=True, blank=True)
    reference = models.CharField(max_length=64, blank=True)
    payer_phone = models.CharField(max_length=32, blank=True)
    payer_name = models.CharField(max_length=128, blank=True)
    narrative = models.TextField(blank=True)
    matched_student = models.ForeignKey('Student', null=True, blank=True, on_delete=models.SET_NULL)
    match_strategy = models.CharField(max_length=16, choices=[('ADMISSION','Admission'),('NAME_CLASS','Name+Class'),('MANUAL','Manual'),('NONE','None')], default='NONE')
    posted_entry = models.ForeignKey('LedgerEntry', null=True, blank=True, on_delete=models.SET_NULL, related_name='import_rows')
    class Meta:
        indexes = [models.Index(fields=['reference']), models.Index(fields=['payer_phone'])]

class NeedsReview(UUIDModel):
    import_row = models.ForeignKey('ImportRow', on_delete=models.CASCADE, related_name='reviews')
    reason = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    resolved_at = models.DateTimeField(null=True, blank=True)

class Expense(UUIDModel):
    MODE = Payment.MODE
    date = models.DateField()
    amount_kes = models.DecimalField(**MONEY, validators=[MinValueValidator(0)])
    category = models.CharField(max_length=64)
    vendor = models.CharField(max_length=128, blank=True)
    mode = models.CharField(max_length=10, choices=MODE)
    term = models.ForeignKey('Term', on_delete=models.PROTECT, related_name='expenses')
    notes = models.TextField(blank=True)

class Budget(UUIDModel):
    term = models.ForeignKey('Term', on_delete=models.CASCADE, related_name='budgets')
    category = models.CharField(max_length=64)
    amount_kes = models.DecimalField(**MONEY, validators=[MinValueValidator(0)])
    class Meta:
        unique_together = ('term','category')

class AuditLog(UUIDModel):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    action = models.CharField(max_length=64)
    entity = models.CharField(max_length=64)
    entity_id = models.CharField(max_length=64)
    meta = models.JSONField(null=True, blank=True)
    at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-at']
