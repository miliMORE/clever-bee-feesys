from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from core.models import UserProfile

DEMO = [
    ('director', 'DIRECTOR', True, 'director@example.com'),
    ('head', 'HEAD', False, 'head@example.com'),
    ('deputy', 'DEPUTY', False, 'deputy@example.com'),
    ('cashier', 'CASHIER', False, 'cashier@example.com'),
]

DEFAULT_PASSWORD = 'ChangeMe123!'

class Command(BaseCommand):
    help = 'Create demo users for Clever Bee with mapped roles/groups.'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        created = 0
        with transaction.atomic():
            for username, role, is_super, email in DEMO:
                u, is_new = User.objects.get_or_create(username=username, defaults={
                    'email': email,
                    'is_staff': True,
                    'is_superuser': is_super,
                })
                if not is_new:
                    u.is_superuser = is_super
                    u.is_staff = True
                    if email and not u.email:
                        u.email = email
                u.set_password(DEFAULT_PASSWORD)
                u.save()
                prof, _ = UserProfile.objects.get_or_create(user=u)
                prof.role = role
                prof.save()
                created += 1 if is_new else 0
        self.stdout.write(self.style.SUCCESS(f'Demo users ready. New: {created}. Default password: {DEFAULT_PASSWORD}'))
