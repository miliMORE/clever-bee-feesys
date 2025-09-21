
# M2 Domain Skeleton (Option A)

Models: Section, ClassLevel, AcademicYear, Term, Student, Enrollment,
FeeItem, FeeStructure (+Line), Invoice (+Line), Payment (+Allocation), AuditLog.
- UUID primary keys
- Decimal(12,2) on all money fields
- Append-only invariants to be enforced at service level in later milestones

## Setup
1) Ensure venv active and Django 5.1.x installed.
2) Run migrations:
   python manage.py makemigrations core
   python manage.py migrate
3) Load sections fixture (optional):
   python manage.py loaddata fixtures/sections.json
4) Create a superuser and explore admin:
   python manage.py createsuperuser

Admin covers all entities with useful filters/search.
