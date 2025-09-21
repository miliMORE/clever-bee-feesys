M3-B — Auth UX polish
---------------------
This pack adds:
- Public login/logout pages (templates/registration/*.html).
- Admin branding (templates/admin/base_site.html).
- Clean redirect after login: /accounts/profile/ -> staff to /admin/, others to /.
- URL wiring for Django's auth views.
- Admin menu label fixes (verbose_name_plural tweaks in models).

Apply:
  1) Expand into repo root:
     Expand-Archive -Path .\M3B_auth_ux_pack.zip -DestinationPath . -Force
  2) No migrations required (labels only). Runserver:
     .\.venv\Scripts\activate
     python manage.py runserver
  3) Visit:
     - /accounts/login/ (login as head/deputy/cashier/director)
     - /admin/ shows branded header.

Revert easily by restoring previous files from Git.
