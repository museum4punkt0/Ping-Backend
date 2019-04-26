import os
from django.test import TestCase
from django.urls import reverse

from main.models import Users
from django.conf import settings

MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'main/fixtures/media')
settings.MEDIA_ROOT += MEDIA_ROOT

class TestSynchronization(TestCase):
    "Synchronization tests"
    fixtures = ['fixtures.json']

    def setUp(self):
        self.url = reverse('synchronise')

    def test_synch_without_user_id(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'error': 'Existing user id must be provided'})

    def test_create_user(self):
        users = Users.objects.all()
        self.assertEqual(len(users), 0)

        response = self.client.get(self.url, {'user_id': 'test_user_id'})
        self.assertEqual(response.status_code, 200)
        users = Users.objects.all()
        self.assertEqual(len(users), 1)
        j_resp = response.json()
        self.assertEqual(j_resp['users']['avatar'], None)
        self.assertEqual(j_resp['users']['category'], None)
        self.assertEqual(j_resp['users']['chats'], [])
        self.assertEqual(j_resp['users']['collections'], [])
        self.assertEqual(j_resp['users']['floor'], 0)
        self.assertEqual(j_resp['users']['language'], 'en')
        self.assertEqual(j_resp['users']['language_style'], None)
        self.assertEqual(j_resp['users']['name'], None)
        self.assertEqual(j_resp['users']['language_style'], None)
        self.assertEqual(j_resp['users']['name'], None)
        self.assertEqual(j_resp['users']['positionX'], '0')
        self.assertEqual(j_resp['users']['positionX'], '0')
        self.assertEqual(j_resp['users']['score'], None)
        self.assertEqual(j_resp['users']['votings'], [])
        self.assertIn('created_at', j_resp['users'])
        self.assertIn('updated_at', j_resp['users'])
        self.assertIn('sync_id', j_resp['users'])
        self.assertNotIn('device_id', j_resp['users'])

