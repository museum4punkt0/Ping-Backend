import os
import json
from uuid import uuid4
from django.urls import reverse
from rest_framework.test import APITestCase
from django.test import TransactionTestCase

from django.conf import settings
from main.models import ObjectsItem, Chats, Votings, Users, Museums

MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'main/fixtures/media')
settings.MEDIA_ROOT = MEDIA_ROOT


class TestSynchronization(APITestCase):
    """Synchronization tests"""
    fixtures = ['fixtures.json']

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('synchronise')
        cls.t_user = 'test_user_id'
        cls.museum_id = str(Museums.objects.first().sync_id)
        cls.url_for_post = cls.url + f'?user_id={cls.t_user}&museum_id={cls.museum_id}'
        cls.object_sync_id = ObjectsItem.objects.all().first().sync_id
        cls.date = '2019-04-18T16:08:41.439Z'

        cls.chat = {
            "sync_id": str(uuid4()),
            "created_at": cls.date,
            "updated_at": cls.date,
            "object_sync_id": str(cls.object_sync_id),
            "finished": False,
            "last_step": False,
            "history": False
        }

        cls.voting = {
            "sync_id": str(uuid4()),
            "created_at": cls.date,
            "updated_at": cls.date,
            "object_sync_id": str(cls.object_sync_id),
            "vote": False
        }

    def test_synch_without_user_id(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'error': 'Existing user id must be provided'})

    def test_create_user(self):
        users = Users.objects.all()
        self.assertEqual(len(users), 1)
        response = self.client.get(self.url, {'user_id': self.t_user,
                                              'museum_id': self.museum_id})
        self.assertEqual(response.status_code, 200)
        users = Users.objects.all()
        self.assertEqual(len(users), 2)
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

    def test_museums(self):
        response = self.client.get(self.url, {'user_id': self.t_user,
                                              'museum_id': self.museum_id})
        self.assertEqual(response.status_code, 200)
        museum = response.json()['museums']
        tensor = museum['tensor'][0]
        object_item = list(filter(lambda x: x.get('id') == 15, museum['objects']))[0]
        category = museum['categories'][0]

        # museum
        self.assertIsInstance(museum['sync_id'], str)
        self.assertIsInstance(museum['floor_amount'], int)
        self.assertIsInstance(tensor['sync_id'], str)
        # self.assertIsInstance(tensor['tensor_flow_model'], str)
        # self.assertIsInstance(tensor['tensor_flow_lables'], str)

        # museum_image
        self.assertIsInstance(museum['images'][0]['id'], int)
        self.assertIsInstance(museum['images'][0]['image'], str)
        self.assertIsInstance(museum['images'][0]['image_type'], str)
        img_types = [image['image_type'] for image in museum['images']]
        self.assertEqual(img_types, ['pnt', '1_map', 'logo'])
        self.assertIsInstance(museum['images'][0]['sync_id'], str)
        self.assertIsInstance(museum['opennings'], dict)

        # museum_object
        self.assertIsInstance(object_item['sync_id'], str)
        self.assertIsInstance(object_item['id'], int)
        self.assertIsInstance(object_item['priority'], int)
        self.assertIsInstance(object_item['floor'], int)
        self.assertIsInstance(object_item['positionX'], str)
        self.assertIsInstance(object_item['positionY'], str)
        self.assertIsInstance(object_item['vip'], bool)
        self.assertIsInstance(object_item['language_style'], str)
        self.assertIsInstance(object_item['avatar'], (str, type(None)))
        self.assertIsInstance(object_item['onboarding'], bool)
        self.assertIsInstance(object_item['object_map'], (str, type(None)))

        # museum_object_localization
        self.assertIsInstance(object_item['localizations'][0]['id'], int)
        self.assertIsInstance(object_item['localizations'][0]['sync_id'], str)
        self.assertIsInstance(object_item['localizations'][0]['language'], str)
        self.assertIsInstance(object_item['localizations'][0]['conversation'],
                              (str, type(None)))
        self.assertIsInstance(object_item['localizations'][0]['phrase'], str)
        self.assertIsInstance(object_item['localizations'][0]['description'], str)
        self.assertIsInstance(object_item['localizations'][0]['title'], str)
        self.assertIsInstance(object_item['localizations'][0]['object_kind'], str)

        # museum_object_image
        self.assertIsInstance(object_item['images'][0]['id'], int)
        self.assertIsInstance(object_item['images'][0]['sync_id'], str)
        self.assertIsInstance(object_item['images'][0]['image'], (str, type(None)))
        self.assertIsInstance(object_item['images'][0]['number'], int)

        # museum_category
        self.assertIsInstance(category['id'], int)
        self.assertIsInstance(category['sync_id'], str)
        self.assertIsInstance(category['sync_object_ids'], list)

        # museum_category_localization
        self.assertIsInstance(category['localizations'][0]['id'], int)
        self.assertIsInstance(category['localizations'][0]['sync_id'], str)
        self.assertIsInstance(category['localizations'][0]['language'], str)
        self.assertIsInstance(category['localizations'][0]['title'], str)

    def test_multimuseums(self):
        pass

    def test_settings(self):
        response = self.client.get(self.url, {'user_id': self.t_user,
                                              'museum_id': self.museum_id})
        self.assertEqual(response.status_code, 200)
        _settings = response.json()['settings']

        self.assertIsInstance(_settings['sync_id'], str)
        self.assertIsInstance(_settings['position_scores'][0]['score'], int)
        self.assertIsInstance(_settings['position_scores'][0]['position'], int)
        self.assertIsInstance(_settings['category_score'], int)
        self.assertIsInstance(_settings['exit_position']['positionX'], int)
        self.assertIsInstance(_settings['exit_position']['positionY'], int)
        self.assertIsInstance(_settings['likes_scores']['like'], int)
        self.assertIsInstance(_settings['likes_scores']['dislike'], int)
        self.assertIsInstance(_settings['chat_scores']['exited'], int)
        self.assertIsInstance(_settings['chat_scores']['finished'], int)
        self.assertIsInstance(_settings['predifined_objects'], list)
        self.assertIsInstance(_settings['priority_scores'][0]['score'], int)
        self.assertIsInstance(_settings['priority_scores'][0]['priority'], int)
        self.assertIsInstance(_settings['distance_scores']['divider'], int)
        self.assertIsInstance(_settings['distance_scores']['basic_point'], int)
        self.assertIsInstance(_settings['languages'], list)
        self.assertIsInstance(_settings['language_styles'], list)

    def test_add_chats(self):
        self.client.get(self.url, {'user_id': self.t_user,
                                   'museum_id': self.museum_id})
        data = {
            "add": {"chats": [self.chat]},
            "delete": {},
            "get": {},
            "update": {}
        }

        chats_count = Chats.objects.count()
        self.assertEqual(chats_count, 1)
        response = self.client.post(self.url_for_post, {'data': json.dumps(data)}, format='multipart')
        self.assertEqual(response.status_code, 200)
        chats_count = Chats.objects.count()
        self.assertEqual(chats_count, 2)

    def test_add_votings(self):
        self.client.get(self.url, {'user_id': self.t_user,
                                   'museum_id': self.museum_id})
        data = {
            "add": {"votings": [self.voting]},
            "delete": {},
            "get": {},
            "update": {}
        }

        voting_count = Votings.objects.count()
        self.assertEqual(voting_count, 1)
        response = self.client.post(self.url_for_post, {'data': json.dumps(data)}, format='multipart')
        self.assertEqual(response.status_code, 200)
        voting_count = Votings.objects.count()
        self.assertEqual(voting_count, 2)

    def test_update_chats(self):
        self.client.get(self.url, {'user_id': self.t_user,
                                   'museum_id': self.museum_id}, format='json')
        data = {
            "add": {"chats": [self.chat]},
            "delete": {},
            "get": {},
            "update": {}
        }

        self.client.post(self.url_for_post, {'data': json.dumps(data)}, format='multipart')

        chat_finished = Chats.objects.all()[1].finished
        self.assertFalse(chat_finished)

        chat = self.chat
        chat['finished'] = True

        data = {
            "add": {},
            "delete": {},
            "get": {},
            "update": {"chats": [chat]}
        }

        response = self.client.post(self.url_for_post, {'data': json.dumps(data)}, format='multipart')
        self.assertEqual(response.status_code, 200)
        chat_finished = Chats.objects.all()[0].finished
        self.assertTrue(chat_finished)


class TestFetch(APITestCase):
    """Fetch tests"""
    fixtures = ['fixtures.json']

    @classmethod
    def setUpTestData(cls):
        cls.t_user = 'test_user_id'
        cls.url_sync = reverse('synchronise')
        cls.url = reverse('fetch')
        cls.museum_id = str(Museums.objects.first().sync_id)

    def setUp(self):
        self.client.get(self.url_sync, {'user_id': self.t_user,
                                    'museum_id': self.museum_id}, format='json')
    def test_fetch_without_user_id(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_fetch_with_user_id_not_exist(self):
        response = self.client.get(self.url, {'user_id': 'not_exist',
                                    'museum_id': self.museum_id}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_museums(self):
        response = self.client.get(self.url, {'user_id': self.t_user,
                                    'museum_id': self.museum_id}, format='json')
        self.assertEqual(response.status_code, 200)
        museum = response.json()['museums']
        tensor = museum['tensor'][0]
        object_item = museum['objects'][3]
        category = museum['categories'][0]

        # museum
        self.assertIsInstance(museum['sync_id'], str)
        self.assertIsInstance(tensor['sync_id'], str)

        # museum_image
        self.assertIsInstance(museum['images'][0]['updated_at'], str)
        self.assertIsInstance(museum['images'][0]['sync_id'], str)

        # museum_object
        self.assertIsInstance(object_item['sync_id'], str)
        self.assertIsInstance(object_item['updated_at'], str)

        # museum_object_localization
        self.assertIsInstance(object_item['localizations'][0]['sync_id'], str)
        self.assertIsInstance(object_item['localizations'][0]['updated_at'], str)

        # museum_object_image
        self.assertIsInstance(object_item['images'][0]['updated_at'], str)
        self.assertIsInstance(object_item['images'][0]['sync_id'], str)

        # museum_category
        self.assertIsInstance(category['updated_at'], str)
        self.assertIsInstance(category['sync_id'], str)

        # museum_category_localization
        self.assertIsInstance(category['localizations'][0]['sync_id'], str)
        self.assertIsInstance(category['localizations'][0]['updated_at'], str)

    def test_settings(self):
        response = self.client.get(self.url, {'user_id': self.t_user,
                                    'museum_id': self.museum_id}, format='json')
        self.assertEqual(response.status_code, 200)
        _settings = response.json()['settings']

        self.assertIsInstance(_settings['sync_id'], str)
        self.assertIsInstance(_settings['updated_at'], str)

    def test_user(self):
        response = self.client.get(self.url, {'user_id': self.t_user,
                                    'museum_id': self.museum_id}, format='json')
        self.assertEqual(response.status_code, 200)
        user = response.json()['users']

        self.assertIsInstance(user['sync_id'], str)
        self.assertIsInstance(user['updated_at'], str)
        self.assertIsInstance(user['collections'], list)
        self.assertIsInstance(user['votings'], list)
        self.assertIsInstance(user['chats'], list)
