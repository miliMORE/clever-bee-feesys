![Clever Bee Academy crest](static/img/cba-logo.png)

# Clever Bee Fee System

Django fee management system for **Clever Bee Academy** (Kenya). Tracks students, term fee structures, payments, ledger entries, bank/M-Pesa import batches, expenses, and budgets — with role-based staff access.

**Current milestone:** M4 (deputy console) in progress, not built yet. See `PROJECT_STATE.md`.

## Stack

- Python + **Django 5.1.x**
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
# Set DJANGO_SECRET_KEY (copy .env.example to .env, or export it in your shell).
# Django does not read .env by itself. For local runserver, set DEBUG=true.
# Generate a key with:
#   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
python manage.py migrate
python manage.py loaddata fixtures/sections.json   # optional
# optional: fixtures/initial_year_terms_levels.json
python manage.py createsuperuser   # or create_demo_users
python manage.py runserver
```

## Deploy (Railway)

`railway.json` `preDeployCommand` (and the Railway service setting) is:

`python manage.py migrate --noinput && python manage.py create_demo_users`

On this Railway Railpack/V2 service that pre-deploy command was set but not executed, so `Procfile` and `railway.json` `startCommand` also run migrate and create_demo_users. `create_demo_users` is create-only, so a second run is safe and does not reset passwords. collectstatic stays in the start command because pre-deploy filesystem changes are not kept:

1. `python manage.py migrate --noinput`
2. `python manage.py create_demo_users`
3. `python manage.py collectstatic --noinput`
4. `gunicorn feesys.wsgi:application --bind 0.0.0.0:$PORT`

Set these environment variables on the service. Do not commit real values.

- `DJANGO_SECRET_KEY` — required when `DEBUG` is off. Long random string.
- `DEBUG` — leave unset or `false` in production. Truthy values are `1`, `true`, `yes`, and `on` (any case). The default is off.
- `ALLOWED_HOSTS` — comma-separated hostnames, such as the Railway domain. Required when `DEBUG` is off.
- `CSRF_TRUSTED_ORIGINS` — comma-separated origins with scheme, such as `https://your-app.up.railway.app`.
- `DATABASE_URL` — Railway Postgres URL. When it is unset, the app uses sqlite at `db.sqlite3`.
- `PORT` — set by Railway. gunicorn binds to it.

`GET /healthz` does not require a login. After `SELECT 1` succeeds it returns HTTP 200 and `{"status":"ok"}`. If that database check fails it returns HTTP 503.

WhiteNoise serves the collected static files. `staticfiles/` is gitignored.

## Project layout

```
feesys/     Django project settings
core/       models, admin, auth bootstrap, services, views
fixtures/   JSON fixtures
templates/  registration + admin branding
scripts/    helper scripts
```

## Status / roadmap notes

Milestones documented in-repo: `docs/history/M2_README.md` (domain skeleton), `docs/history/M3_README.txt` / `docs/history/M3B_README.txt` (auth & UX). Do not invent unbuilt M4+ features — see `PROJECT_STATE.md`.
