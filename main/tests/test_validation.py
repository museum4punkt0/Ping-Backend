from uuid import uuid4

from rest_framework.test import APITestCase

from main.models import Chats, Votings, ObjectsItem, Categories, Users
from main.views.validators import validate_common_fields, validate_chats, \
    validate_collections, validate_user, validate_votings


class TestValidateCommonFields(APITestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        obj = Chats.objects.get(id=1)

        self.data = {
            'entity_name': 'test',
            'data': {},
            'action': 'test',
            'entity_sync_id': str(obj.sync_id),
            'sync_ids': [],
            'o_model': Chats,
            'created_at': '2019-04-18T16:08:41.439Z',
            'updated_at': '2019-04-18T16:08:41.439Z',
            'ob_sync_id': str(obj.objects_item.sync_id)
        }

    def test_required_fields(self):
        errors = validate_common_fields(entity_name='test', data={}, action='test')
        self.assertEqual(len(errors), 5)

    def test_valid_data(self):
        errors = validate_common_fields(**self.data)
        self.assertEqual(len(errors), 0)

    def test_entity_sync_id_validation(self):
        self.data['entity_sync_id'] = 'error'
        errors = validate_common_fields(**self.data)
        self.assertEqual(len(errors), 1)

    def test_created_at_validation(self):
        self.data['created_at'] = 'error'
        errors = validate_common_fields(**self.data)
        self.assertEqual(len(errors), 1)

    def test_updated_at_validation(self):
        self.data['updated_at'] = 'error'
        errors = validate_common_fields(**self.data)
        self.assertEqual(len(errors), 1)

    def test_ob_sync_id_validation(self):
        self.data['ob_sync_id'] = 'error'
        errors = validate_common_fields(**self.data)
        self.assertEqual(len(errors), 1)

        self.data['ob_sync_id'] = str(uuid4())
        errors = validate_common_fields(**self.data)
        self.assertEqual(len(errors), 1)

    def test_add_action(self):
        self.data['action'] = 'add'
        errors = validate_common_fields(**self.data)
        self.assertEqual(len(errors), 1)

        self.data['entity_sync_id'] = str(uuid4())
        errors = validate_common_fields(**self.data)
        self.assertEqual(len(errors), 0)


class TestValidateChats(APITestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        obj = Chats.objects.get(id=1)

        self.data = {
            'user': 1,
            'errors': {'add_errors': [], 'update_errors': []},
            'data': {},
            'action': 'update',
            'ch_sync_id': str(obj.sync_id),
            'created_at': '2019-04-18T16:08:41.439Z',
            'updated_at': '2019-04-18T16:08:41.439Z',
            'ob_sync_id': str(obj.objects_item.sync_id),
            'finished': 'false',
            'planned': False,
            'last_step': 0,
            'history': False,
        }

    def test_valid_data(self):
        data, errors = validate_chats(**self.data)
        self.assertEqual(len(errors['update_errors']), 0)

    def test_required_fields(self):
        self.data['finished'] = None
        self.data['last_step'] = None
        self.data['history'] = None

        data, errors = validate_chats(**self.data)
        self.assertEqual(len(errors['update_errors']), 3)

    def test_finished_validation(self):
        # self.data['finished'] = 4
        # data, errors1 = validate_chats(**self.data)
        # self.assertEqual(len(errors1['update_errors']), 1)

        self.data['finished'] = 'invalid'
        data, errors = validate_chats(**self.data)
        self.assertEqual(len(errors['update_errors']), 1)

    def test_last_step(self):
        self.data['last_step'] = 'invalid'
        data, errors = validate_chats(**self.data)
        self.assertEqual(len(errors['update_errors']), 1)


class TestValidateVotings(APITestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        obj = Votings.objects.get(id=1)

        self.data = {
            'user': 1,
            'errors': {'add_errors': [], 'update_errors': []},
            'data': {},
            'action': 'update',
            'vt_sync_id': str(obj.sync_id),
            'created_at': '2019-04-18T16:08:41.439Z',
            'updated_at': '2019-04-18T16:08:41.439Z',
            'ob_sync_id': str(obj.objects_item.sync_id),
            'vote': 'false',
        }

    def test_valid_data(self):
        data, errors = validate_votings(**self.data)
        self.assertEqual(len(errors['update_errors']), 0)

    def test_required_fields(self):
        self.data['vote'] = None

        data, errors = validate_votings(**self.data)
        self.assertEqual(len(errors['update_errors']), 1)

    def test_vote_validation(self):
        # self.data['vote'] = 4
        # data, errors1 = validate_votings(**self.data)
        # self.assertEqual(len(errors1['update_errors']), 1)

        self.data['vote'] = 'invalid'
        data, errors = validate_votings(**self.data)
        self.assertEqual(len(errors['update_errors']), 1)


class TestValidateCollections(APITestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        ob_sync_id = ObjectsItem.objects.get(id=38).sync_id
        self.ct_sync_id1 = Categories.objects.get(id=8).sync_id
        self.ct_sync_id2 = Categories.objects.get(id=9).sync_id

        self.data = {
            'user': 1,
            'errors': {'add_errors': [], 'update_errors': []},
            'data': {'category': []},
            'action': 'update',
            'cl_sync_id': str(uuid4()),
            'created_at': '2019-04-18T16:08:41.439Z',
            'updated_at': '2019-04-18T16:08:41.439Z',
            'ob_sync_id': str(ob_sync_id),
            'image': 'error',
            'ctgrs': str(self.ct_sync_id1)
        }

    def test_required_fields(self):
        self.data['image'] = None
        self.data['ctgrs'] = None

        data, errors = validate_collections(**self.data)
        self.assertEqual(len(errors['update_errors']), 2)

    def test_image_validation(self):
        data, errors = validate_collections(**self.data)
        self.assertEqual(len(errors['update_errors']), 1)

    def test_ctgrs_validation_with_invalid_category(self):
        self.data['ctgrs'] = 'error'
        data, errors = validate_collections(**self.data)
        self.assertEqual(len(errors['update_errors']), 3)

    def test_ctgrs_validation_with_valid_category(self):
        self.data['ctgrs'] = [str(self.ct_sync_id1), str(self.ct_sync_id2)]
        data, errors = validate_collections(**self.data)
        self.assertEqual(len(errors['update_errors']), 1)

    def test_ctgrs_validation_with_invalid_one_category(self):
        self.data['ctgrs'] = [str(uuid4()), str(self.ct_sync_id2)]
        data, errors = validate_collections(**self.data)
        self.assertEqual(len(errors['update_errors']), 2)


class TestValidateUser(APITestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        ct_sync_id = Categories.objects.get(id=8).sync_id
        user = Users.objects.get(id=1)

        self.data = {
            'errors': {'add_errors': [], 'update_errors': []},
            'data': {},
            'user': user,
            'action': 'update',
            'us_sync_id': str(user.sync_id),
            'created_at': '2019-04-18T16:08:41.439Z',
            'updated_at': '2019-04-18T16:08:41.439Z',
            'name': 'Test',
            'avatar': None,
            'category': str(ct_sync_id),
            'positionx': 1,
            'positiony': 1,
            'floor': 1,
            'language': 'en',
            'language_style': [],
            'score': None,
            'device_id': None
        }

    def test_valid_data(self):
        data, errors = validate_user(**self.data)
        self.assertEqual(len(errors['update_errors']), 0)

    def test_required_fields(self):
        self.data['positionx'] = None
        self.data['positiony'] = None
        self.data['floor'] = None
        self.data['language'] = None
        self.data['language_style'] = None

        data, errors = validate_user(**self.data)
        self.assertEqual(len(errors['update_errors']), 5)

    def test_positionx_validation(self):
        from main.views.validators import POSITION_RANGE

        self.data['positionx'] = [1]
        data, errors = validate_user(**self.data)
        self.assertEqual(len(errors['update_errors']), 1)

        self.data['errors']['update_errors'] = []
        self.data['positionx'] = POSITION_RANGE['x'][0] - 1
        data, errors = validate_user(**self.data)
        self.assertEqual(len(errors['update_errors']), 1)

        self.data['errors']['update_errors'] = []
        self.data['positionx'] = POSITION_RANGE['x'][1] + 1
        data, errors = validate_user(**self.data)
        self.assertEqual(len(errors['update_errors']), 1)

    def test_positiony_validation(self):
        from main.views.validators import POSITION_RANGE

        self.data['positiony'] = 'error'
        data, errors = validate_user(**self.data)
        self.assertEqual(len(errors['update_errors']), 1)

        self.data['errors']['update_errors'] = []
        self.data['positiony'] = POSITION_RANGE['y'][0] - 1
        data, errors = validate_user(**self.data)
        self.assertEqual(len(errors['update_errors']), 1)

        self.data['errors']['update_errors'] = []
        self.data['positiony'] = POSITION_RANGE['y'][1] + 1
        data, errors = validate_user(**self.data)
        self.assertEqual(len(errors['update_errors']), 1)

    def test_floor_validation(self):
        self.data['floor'] = 'error'
        data, errors = validate_user(**self.data)
        self.assertEqual(len(errors['update_errors']), 1)

    def test_language_validation(self):
        self.data['language'] = 'error'
        data, errors = validate_user(**self.data)
        self.assertEqual(len(errors['update_errors']), 1)

    def test_language_style_validation(self):
        self.data['language_style'] = 'error'
        data, errors = validate_user(**self.data)
        self.assertEqual(len(errors['update_errors']), 1)
