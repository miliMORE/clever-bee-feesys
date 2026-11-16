from io import StringIO
from unittest.mock import patch

from django.contrib.auth import authenticate, get_user_model
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase

from core.management.commands.create_demo_users import DEFAULT_PASSWORD


def _user_snapshot(user):
    user.refresh_from_db()
    return {
        'password': user.password,
        'is_superuser': user.is_superuser,
        'is_staff': user.is_staff,
        'groups': tuple(user.groups.order_by('name').values_list('name', flat=True)),
        'email': user.email,
        'role': user.profile.role,
    }


class CreateDemoUsersTests(TestCase):
    def test_second_run_does_not_change_existing_user(self):
        call_command('create_demo_users', stdout=StringIO())
        User = get_user_model()
        director = User.objects.get(username='director')
        self.assertTrue(director.is_superuser)
        self.assertTrue(director.is_staff)
        self.assertEqual(director.profile.role, 'DIRECTOR')
        self.assertEqual(
            tuple(director.groups.order_by('name').values_list('name', flat=True)),
            ('DIRECTOR',),
        )

        user = User.objects.get(username='head')
        user.profile.role = 'CASHIER'
        user.profile.save()
        user.email = 'head-kept@example.com'
        user.is_superuser = True
        user.is_staff = False
        user.groups.clear()
        user.save()
        before = _user_snapshot(user)

        output = StringIO()
        call_command('create_demo_users', stdout=output)
        self.assertEqual(_user_snapshot(user), before)
        text = output.getvalue()
        self.assertIn('Skipped head (already exists).', text)
        self.assertIn('Created: 0. Skipped: 4.', text)

    def test_changed_password_survives_rerun(self):
        call_command('create_demo_users', stdout=StringIO())
        User = get_user_model()
        user = User.objects.get(username='deputy')
        user.set_password('A-New-Password-99')
        user.save()
        before = _user_snapshot(user)

        call_command('create_demo_users', stdout=StringIO())
        self.assertEqual(_user_snapshot(user), before)
        self.assertIsNotNone(authenticate(username='deputy', password='A-New-Password-99'))
        self.assertIsNone(authenticate(username='deputy', password=DEFAULT_PASSWORD))

    def test_missing_user_is_created_on_later_run(self):
        call_command('create_demo_users', stdout=StringIO())
        User = get_user_model()
        User.objects.filter(username='cashier').delete()
        kept = {
            username: _user_snapshot(User.objects.get(username=username))
            for username in ('director', 'head', 'deputy')
        }

        output = StringIO()
        call_command('create_demo_users', stdout=output)
        text = output.getvalue()
        self.assertIn('Created cashier.', text)
        self.assertIn('Created: 1. Skipped: 3.', text)
        for username in ('director', 'head', 'deputy'):
            self.assertIn(f'Skipped {username} (already exists).', text)
            self.assertEqual(_user_snapshot(User.objects.get(username=username)), kept[username])

        cashier = User.objects.get(username='cashier')
        self.assertTrue(cashier.is_staff)
        self.assertFalse(cashier.is_superuser)
        self.assertEqual(cashier.email, 'cashier@example.com')
        self.assertEqual(cashier.profile.role, 'CASHIER')
        self.assertEqual(
            tuple(cashier.groups.order_by('name').values_list('name', flat=True)),
            ('CASHIER',),
        )
        self.assertIsNotNone(authenticate(username='cashier', password=DEFAULT_PASSWORD))


class HomePageTests(TestCase):
    def test_anonymous_home_has_login_link(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Clever Bee Academy Fees System')
        self.assertContains(response, 'cba-logo.png')
        self.assertContains(response, '/accounts/login/')
        self.assertContains(response, 'Log in')
        self.assertNotContains(response, 'Blueprint-compliant M2 build is installed.')
        self.assertNotContains(response, 'Dashboard')

    def test_staff_home_links_to_dashboard(self):
        user = get_user_model().objects.create_user(
            username='staffer',
            password='staff-pass',
            is_staff=True,
        )
        self.client.force_login(user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/admin/"')
        self.assertContains(response, 'Dashboard')
        self.assertNotContains(response, '/accounts/login/')

    def test_nonstaff_home_links_to_home_dashboard(self):
        user = get_user_model().objects.create_user(
            username='guardian',
            password='guardian-pass',
            is_staff=False,
        )
        self.client.force_login(user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/"')
        self.assertContains(response, 'Dashboard')
        self.assertNotContains(response, '/accounts/login/')
        self.assertNotContains(response, '/admin/')


class HealthzTests(TestCase):
    def test_healthz_returns_ok_when_database_responds(self):
        response = self.client.get('/healthz')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})

    def test_healthz_trailing_slash_returns_ok(self):
        response = self.client.get('/healthz/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})

    def test_healthz_returns_503_when_database_check_fails(self):
        with patch('core.views.connection.cursor', side_effect=OperationalError('down')):
            response = self.client.get('/healthz')
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {'status': 'unavailable'})
