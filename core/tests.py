from unittest.mock import patch

from django.db.utils import OperationalError
from django.test import TestCase


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
