M3 — Auth, Groups, Permissions, Demo Users (ZIP-3)
--------------------------------------------------
This pack adds:
- Groups: DIRECTOR, HEAD, DEPUTY, CASHIER (created on migrate via post_migrate).
- UserProfile (role ↔ group sync via signal).
- Management command `create_demo_users`.
- Edit-limit scaffolding service (not wired yet).

Post-merge commands:
  .\\.venv\\Scripts\\activate
  python manage.py migrate
  python manage.py create_demo_users
  python manage.py runserver

Login (default passwords all `ChangeMe123!`):
  director / head / deputy / cashier
