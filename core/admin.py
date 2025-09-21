from django.contrib import admin
from . import models

@admin.register(models.ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):
    list_display = ('name','section','order')
    list_filter = ('section',)
    search_fields = ('name',)

@admin.register(models.AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(models.Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('year','number','start_date','end_date')
    list_filter = ('year','number')

@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('admission_no','last_name','first_name','boarding_status','status')
    list_filter = ('status','boarding_status')
    search_fields = ('admission_no','first_name','last_name')

@admin.register(models.FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('term','class_level','boarding_status','amount_kes')
    list_filter = ('term__year','term__number','class_level__section','boarding_status')
    search_fields = ('class_level__name',)

@admin.register(models.LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ('date','student','term','entry_type','source','mode','amount_kes','reference')
    list_filter = ('entry_type','source','mode','term__year','term__number')
    search_fields = ('student__admission_no','reference','memo')

@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('date','student','term','mode','amount_kes','edit_count_today')
    list_filter = ('mode','term__year','term__number')
    search_fields = ('student__admission_no','reference')

@admin.register(models.PaymentEditLog)
class PaymentEditLogAdmin(admin.ModelAdmin):
    list_display = ('payment','edited_by','edited_at')

@admin.register(models.ImportBatch)
class ImportBatchAdmin(admin.ModelAdmin):
    list_display = ('channel','filename','imported_by','imported_at','status')
    list_filter = ('channel','status')

@admin.register(models.ImportRow)
class ImportRowAdmin(admin.ModelAdmin):
    list_display = ('batch','date','amount','reference','payer_name','matched_student','match_strategy')
    list_filter = ('match_strategy',)
    search_fields = ('reference','payer_name','payer_phone')

@admin.register(models.NeedsReview)
class NeedsReviewAdmin(admin.ModelAdmin):
    list_display = ('import_row','reason','resolved_by','resolved_at')

@admin.register(models.Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date','term','category','amount_kes','mode','vendor')
    list_filter = ('term__year','term__number','category','mode')

@admin.register(models.Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('term','category','amount_kes')
    list_filter = ('term__year','term__number','category')

@admin.register(models.AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('at','actor','action','entity','entity_id')
    list_filter = ('action','entity','at')
    search_fields = ('actor__username','entity','entity_id')
