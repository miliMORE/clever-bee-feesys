# Clever Bee Fee System

Django fee management system for **Clever Bee Academy** (Kenya). Tracks students, term fee structures, payments, ledger entries, bank/M-Pesa import batches, expenses, and budgets — with role-based staff access.

**Current milestone:** M3 (auth, groups, permissions, demo users) per `PROJECT_STATE.md`.

## Stack

- Python + **Django 5.1.***
- UUID primary keys; `Decimal(12,2)` money fields
- Django admin + simple auth UX (`/accounts/login/`)
- Fixtures for sections / year-term-levels

## Domain model (verified in `core/models.py`)

- **Organisation / academics:** `ClassLevel` (ECDE, Lower/Upper Primary, Junior Secondary), `AcademicYear`, `Term`
- **Students:** admission no., guardians/contacts, boarding status, enrollment class/term/year
- **Fees:** `FeeStructure` per term × class × boarding
- **Money movement:** `LedgerEntry` (invoice / payment / reversal), `Payment`, `PaymentEditLog`
- **Imports:** `ImportBatch` / `ImportRow` (Bank or M-Pesa CSV channels), `NeedsReview`
- **Ops:** `Expense`, `Budget`, `AuditLog`
- **Access:** `UserProfile` roles — Director, Head Teacher, Deputy Head, Cashier (synced to Django groups)

## Auth (M3 / M3-B)

Groups created on migrate: `DIRECTOR`, `HEAD`, `DEPUTY`, `CASHIER`.

```bash
python manage.py migrate
python manage.py create_demo_users
python manage.py runserver
```

Demo logins (default password `ChangeMe123!`): `director`, `head`, `deputy`, `cashier`.

- Login: `/accounts/login/`
- Staff redirect toward `/admin/` after login
- Edit-limit scaffolding exists (`core/services/edit_limits.py`) but is not fully wired yet

## Setup

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\activate
# Unix:    source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixtures/sections.json   # optional
# optional: fixtures/initial_year_terms_levels.json
python manage.py createsuperuser   # or create_demo_users
python manage.py runserver
```

## Project layout

```
feesys/     Django project settings
core/       models, admin, auth bootstrap, services, views
fixtures/   JSON fixtures
templates/  registration + admin branding
scripts/    helper scripts
```

## Status / roadmap notes

Milestones documented in-repo: `M2_README.md` (domain skeleton), `M3_README.txt` / `M3B_README.txt` (auth & UX). Do not invent unbuilt M4+ features — see `PROJECT_STATE.md`.
