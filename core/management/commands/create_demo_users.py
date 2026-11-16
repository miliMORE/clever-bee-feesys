from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from core.models import UserProfile

DEMO = [
    ('director', 'DIRECTOR', True, 'director@example.com'),
    ('head', 'HEAD', False, 'head@example.com'),
    ('deputy', 'DEPUTY', False, 'deputy@example.com'),
    ('cashier', 'CASHIER', False, 'cashier@example.com'),
]

DEFAULT_PASSWORD = 'ChangeMe123!'


class Command(BaseCommand):
    help = 'Create missing demo users. Existing usernames are left unchanged.'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        created = 0
        skipped = 0
        for username, role, is_super, email in DEMO:
            if User.objects.filter(username=username).exists():
                skipped += 1
                self.stdout.write(f'Skipped {username} (already exists).')
                continue
            try:
                with transaction.atomic():
                    user = User(
                        username=username,
                        email=email,
                        is_staff=True,
                        is_superuser=is_super,
                    )
                    user.set_password(DEFAULT_PASSWORD)
                    user.save()
                    profile, _ = UserProfile.objects.get_or_create(user=user)
                    profile.role = role
                    profile.save()
            except IntegrityError:
                skipped += 1
                self.stdout.write(f'Skipped {username} (already exists).')
                continue
            created += 1
            self.stdout.write(self.style.SUCCESS(f'Created {username}.'))
        self.stdout.write(self.style.SUCCESS(
            f'Demo users ready. Created: {created}. Skipped: {skipped}.'
        ))
