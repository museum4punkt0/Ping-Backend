import distutils
import datetime
import uuid
import base64
from PIL import Image
from io import BytesIO
from django.core.files.temp import NamedTemporaryFile
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from operator import itemgetter
from main.models import (
    Collections,
    Votings,
    Users,
    Settings,
    Museums,
    ObjectsItem,
    Categories,
    Chats,
    MuseumsImages,
    ObjectsLocalizations,
    ObjectsImages
)
import logging

from main.serializers import (
    CollectionsSerializer,
    UsersSerializer,
    SettingsSerializer,
    MuseumsSerializer,
    MuseumsImagesSerializer,
    ObjectsItemSerializer,
    CategoriesSerializer,
    ChatsSerializer,
    PredefinedAvatarsSerializer,
    MuseumsImagesSerializer,
    ObjectsItemSerializer,
    CategorieslocalizationsSerializer, 
    ObjectsCategoriesSerializer,
    ObjectsLocalizationsSerializer,
    ObjectsImagesSerializer,
    UsersSerializer
    )
from main.views.validators import validate_common_fields
from mein_objekt.settings import DEFAULT_MUSEUM

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.ERROR)

def serialized_data(museum, user=None, settings=None, categories=None):
    data = {'museums': None,
            'users': None,
            'settings': None}

    # museum serialization
    serialized_museum = MuseumsSerializer(museum).data
    museum_table = {'id': None,
                    'images': [],
                    'objects': [],
                    'categories': []}

    museum_table['id'] = serialized_museum['id']

    serialized_museumsimages = serialized_museum['museumimages']
    for image in serialized_museumsimages:
        image_dict = {}
        image_dict['id'] = image['id']
        image_dict['image_type'] = image['image_type']
        image_dict['image'] = image['image']
        image_dict['sync_id'] = image['sync_id']
        image_dict['synced'] = image['synced']
        image_dict['created_at'] = image['created_at']
        image_dict['updated_at'] = image['updated_at']
        museum_table['images'].append(image_dict)

    serialized_objects_items = serialized_museum['objectsitems']
    for item in serialized_objects_items:
        item_table = {'id': None,
                      'priority': None,
                      'floor': None,
                      'positionX': None,
                      'positionY': None,
                      'vip': None,
                      'language_style': None,
                      'avatar': None,
                      'onboarding': None,
                      'object_map': None,
                      'sync_id': None,
                      'synced': None,
                      'created_at': None,
                      'updated_at': None,
                      'localizations': [],
                      'images': []}

        item_table['id'] = item['id']
        item_table['priority'] = item['priority']
        item_table['floor'] = item['floor']
        item_table['positionX'] = item['positionx']
        item_table['positionY'] = item['positiony']
        item_table['vip'] = item['vip']
        item_table['language_style'] = item['language_style']
        item_table['avatar'] = item['avatar']
        item_table['onboarding'] = item['onboarding']
        item_table['object_map'] = item['object_map']
        item_table['sync_id'] = item['sync_id']
        item_table['synced'] = item['synced']
        item_table['created_at'] = item['created_at']
        item_table['updated_at'] = item['updated_at']

        localizations = item['localizations']
        for local in localizations:
            local_dict = {}
            local_dict['id'] = local['id']
            local_dict['language'] = local['language']
            local_dict['conversation'] = local['conversation']
            local_dict['phrase'] = local['phrase']
            local_dict['description'] = local['description']
            local_dict['title'] = local['title']
            local_dict['object_kind'] = local['object_kind']
            local_dict['sync_id'] = local['sync_id']
            local_dict['synced'] = local['synced']
            local_dict['created_at'] = local['created_at']
            local_dict['updated_at'] = local['updated_at']
            item_table['localizations'].append(local_dict)

        serialized_images = item['images']
        for image in serialized_images:
            image_dict = {}
            image_dict['id'] = image['id']
            image_dict['image'] = image['image']
            image_dict['sync_id'] = image['sync_id']
            image_dict['synced'] = image['synced']
            image_dict['created_at'] = image['created_at']
            image_dict['updated_at'] = image['updated_at']
            item_table['images'].append(image_dict)
        museum_table['objects'].append(item_table)

    for category in categories:
        serialized_category = CategoriesSerializer(category).data
        category_table = {'id': None,
                          'object_ids': [],
                          'sync_object_ids': [],
                          'localizations': [],
                          'sync_id': None,
                          'synced': None,
                          'created_at': None,
                          'updated_at': None}

        category_table['id'] = serialized_category['id']

        objects = category.objectscategories_set.all()
        category_table['object_ids'] = [i.objects_item.id for i in objects]
        category_table['sync_object_ids'] = [str(i.objects_item.sync_id) for i in objects]

        localizations = serialized_category['localizations']
        for local in localizations:
            local_dict = {}
            local_dict['id'] = local['id']
            local_dict['language'] = local['language']
            local_dict['title'] = local['title']
            local_dict['sync_id'] = local['sync_id']
            local_dict['synced'] = local['synced']
            local_dict['created_at'] = local['created_at']
            local_dict['updated_at'] = local['updated_at']
            category_table['localizations'].append(local_dict)

        category_table['sync_id'] = serialized_category['sync_id']
        category_table['synced'] = serialized_category['synced']
        category_table['created_at'] = serialized_category['created_at']
        category_table['updated_at'] = serialized_category['updated_at']
        museum_table['categories'].append(category_table)

    data['museums'] = museum_table

    # user serialization
    if user:
        serialized_user = UsersSerializer(user).data
        user_table = {'id': None,
                      'name': None,
                      'avatar': None,
                      'category': None,
                      'positionX': None,
                      'positionY': None,
                      'floor': None,
                      'language': None,
                      'language_style': None,
                      'score': None,
                      'sync_id': None,
                      'synced': None,
                      'created_at': None,
                      'updated_at': None,
                      'chats': [],
                      'votings': [],
                      'collections': []
                      }

        user_table['id'] = serialized_user['id']
        user_table['name'] = serialized_user['name']
        user_table['avatar'] = serialized_user['avatar']
        user_table['category'] = serialized_user['category']
        user_table['positionX'] = serialized_user['positionx']
        user_table['positionY'] = serialized_user['positiony']
        user_table['floor'] = serialized_user['floor']
        user_table['language'] = serialized_user['language']
        user_table['language_style'] = user.userslanguagestyles.language_style
        user_table['score'] = user.userslanguagestyles.score
        user_table['sync_id'] = serialized_user['sync_id']
        user_table['synced'] = serialized_user['synced']
        user_table['created_at'] = serialized_user['created_at']
        user_table['updated_at'] = serialized_user['updated_at']

        serialized_chats = serialized_user['chats']
        for chat in serialized_chats:
            chat_dict = {}
            chat_dict['id'] = chat['id']
            chat_dict['object_id'] = chat['objects_item']
            chat_dict['last_step'] = chat['last_step']
            chat_dict['finished'] = chat['finished']
            chat_dict['history'] = chat['history']
            chat_dict['sync_id'] = chat['sync_id']
            chat_dict['synced'] = chat['synced']
            chat_dict['created_at'] = chat['created_at']
            chat_dict['updated_at'] = chat['updated_at']
            user_table['chats'].append(chat_dict)

        serialized_votings = serialized_user['votings']
        for vote in serialized_votings:
            vote_dict = {}
            vote_dict['id'] = vote['id']
            vote_dict['object_id'] = vote['objects_item']
            vote_dict['vote'] = vote['vote']
            vote_dict['sync_id'] = vote['sync_id']
            vote_dict['synced'] = vote['synced']
            vote_dict['created_at'] = vote['created_at']
            vote_dict['updated_at'] = vote['updated_at']
            user_table['votings'].append(vote_dict)

        serialized_collections = serialized_user['collections']
        for collection in serialized_collections:
            collection_dict = {}
            collection_dict['object_id'] = collection['objects_item']
            collection_dict['image'] = collection['image']
            collection_dict['category'] = collection['category']
            collection_dict['sync_id'] = collection['sync_id']
            collection_dict['synced'] = collection['synced']
            collection_dict['created_at'] = collection['created_at']
            collection_dict['updated_at'] = collection['updated_at']
            user_table['collections'].append(collection_dict)
        data['users'] = user_table
    else:
        data['users'] = None

    # settings serialization
    if settings:
        for setting in settings:
            serialized_settings = SettingsSerializer(setting).data
            settings_table = {'id': None,
                              'position_scores': None,
                              'category_score': None,
                              'exit_position': None,
                              'likes_scores': None,
                              'chat_scores': None,
                              'predifined_objects': [],
                              'priority_scores': None,
                              'distance_scores': None,
                              'predefined_categories': None,
                              'predefined_avatars': None,
                              'languages': [],
                              'sync_id': None,
                              'synced': None,
                              'created_at': None,
                              'updated_at': None}

            settings_table['id'] = serialized_settings['id']
            settings_table['position_scores'] = serialized_settings['position_score']
            settings_table['category_score'] = serialized_settings['category_score']
            settings_table['exit_position'] = serialized_settings['exit_position']
            settings_table['likes_scores'] = serialized_settings['likes_score']
            settings_table['chat_scores'] = serialized_settings['chat_score']
            settings_table['predifined_objects'] = [str(i.predefined_object.sync_id) for i in setting.settingspredefinedobjectsitems_set.all()]
            settings_table['priority_scores'] = serialized_settings['priority_score']
            settings_table['distance_scores'] = serialized_settings['distance_score']
            settings_table['predefined_avatars'] = [i['image'] for i in serialized_settings['predefined_avatars']]
            settings_table['languages'] = serialized_settings['languages']
            settings_table['sync_id'] = serialized_settings['sync_id']
            settings_table['synced'] = serialized_settings['synced']
            settings_table['created_at'] = serialized_settings['created_at']
            settings_table['updated_at'] = serialized_settings['updated_at']
            data['settings'] = settings_table
    else:
        data['settings'] = None

    return data


class Synchronization(APIView):

    def get(self, request, format=None):
        user_id = request.GET.get('user_id', None)
        if user_id:
            user = Users.objects.get(device_id=user_id)
        else:
            return JsonResponse({'error': 'user id must be passed'}, safe=True)

        museum = Museums.objects.get(name=DEFAULT_MUSEUM)
        settings = (museum.settings,)
        categories = Categories.objects.all()

        if not settings:
          return JsonResponse({'error': 'museums settings must be defined'}, safe=True)

        return JsonResponse(serialized_data(museum, user, settings, categories), safe=True)

    def post(self, request, format=None):
        user_id = request.GET.get('user_id', None)
        if user_id:
            user = Users.objects.get(device_id=user_id)
        else:
            return JsonResponse({'error': 'user id must be passed'}, safe=True)

        post_data = request.data
        get_values = post_data.get('get')
        add_values = post_data.get('add')
        objects_sync_ids = []
        categories_sync_ids = []

        # traverse 'get' table
        museum = Museums.objects.get(name=DEFAULT_MUSEUM)
        if get_values.get('objects'):
            objects_sync_ids.extend(get_values.get('objects'))

        if get_values.get('object_images'):
            images_objects = ObjectsItem.objects.filter(objectsimages__sync_id__in=get_values.get('object_images'))
            objects_sync_ids.extend([str(i.sync_id) for i in images_objects])

        if get_values.get('object_localizations'):
            local_objects = ObjectsItem.objects.filter(objectslocalizations__sync_id__in=get_values.get('object_localizations'))
            objects_sync_ids.extend([str(i.sync_id) for i in local_objects])

        museum.objects_to_serialize = list(set(objects_sync_ids))

        if get_values.get('categories'):
            categories_sync_ids.extend(get_values.get('categories'))

        if get_values.get('category_localizations'):
            local_categories = Categories.objects.filter(categorieslocalizations__sync_id__in=get_values.get('category_localizations'))
            categories_sync_ids.extend([str(i.sync_id) for i in local_categories])

        categories = Categories.objects.filter(sync_id__in=categories_sync_ids)
        settings = Settings.objects.filter(sync_id__in=get_values.get('settings', []))

        # traverse 'add' values
        chats, votings, collections = None, None, None
        errors = {'errors': []}

        if add_values:
            chats = add_values.get('chats')
            votings = add_values.get('votings')
            collections = add_values.get('collections')
            chats_objects = []
            csync_ids = []
            votings_objects = []
            vsync_ids = []
            collections_objects = []
            clsync_ids = []

        if chats:
            data = {'user': None,
                    'objects_item': None,
                    'finished': None,
                    'history': None,
                    'last_step': None,
                    'sync_id': None,
                    'created_at': None,
                    'updated_at': None}

            for chat in chats:
                ch_sync_id = chat.get('sync_id')
                created_at = chat.get('created_at')
                updated_at = chat.get('updated_at')
                ob_sync_id = chat.get('object_sync_id')
                finished = chat.get('finished')
                history = chat.get('history')
                last_step = chat.get('last_step')
                uuid_obj = None

                c_errors = validate_common_fields('chat',
                                                   data,
                                                   Chats,
                                                   csync_ids,
                                                   entity_sync_id=ch_sync_id,
                                                   created_at=created_at,
                                                   updated_at=updated_at,
                                                   ob_sync_id=ob_sync_id)
                errors['errors'].extend(c_errors)

                if finished:
                    try:
                        bl = bool(distutils.util.strtobool(finished))
                        data['finished'] = bl
                    except:
                        logging.error(f'Inappropriate "finished":{finished} (type:{type(finished)}) bool value for chat {ch_sync_id} sync_id')
                        errors['errors'].append({'chat': f'Inappropriate "finished" bool value for chat {ch_sync_id} sync_id'})
                else:
                    errors['errors'].append({'chat': f'Value "finished" for chat {ch_sync_id} is required'})

                if history:
                    data['history'] = history
                else:
                    errors['errors'].append({'chat': f'Value "history" for chat {ch_sync_id} is required'})

                if last_step:
                    try:
                        ls = int(last_step)
                        data['last_step'] = ls
                    except:
                        errors['errors'].append({'chat': f'Inappropriate "last step" integer value for chat {ch_sync_id} sync_id'})
                else:
                    errors['errors'].append({'chat': f'Value "finished" for chat {ch_sync_id} is required'})

                data['user'] = user

                try:
                    chats_objects.append(Chats(**data))
                except Exception as e:
                    errors['errors'].append({'chat': e.args})

        if votings:
            for voting in votings:
                data = {'user': None,
                        'objects_item': None,
                        'vote': None,
                        'sync_id': None,
                        'created_at': None,
                        'updated_at': None}

                vt_sync_id = voting.get('sync_id')
                created_at = voting.get('created_at')
                updated_at = voting.get('updated_at')
                ob_sync_id = voting.get('object_sync_id')
                vote = voting.get('vote')
                uuid_obj = None

                c_errors = validate_common_fields('vote',
                                                   data,
                                                   Votings,
                                                   vsync_ids,
                                                   entity_sync_id=vt_sync_id,
                                                   created_at=created_at,
                                                   updated_at=updated_at,
                                                   ob_sync_id=ob_sync_id)
                errors['errors'].extend(c_errors)

                if vote:
                    try:
                        bl = bool(distutils.util.strtobool(vote))
                        data['vote'] = bl
                    except:
                        errors['errors'].append({'vote': f'Inappropriate "vote" bool value for chat {vt_sync_id} sync_id'})
                else:
                    errors['errors'].append({'vote': f'Value "vote" for vote {vt_sync_id} is required'})

                data['user'] = user

                try:
                    votings_objects.append(Votings(**data))
                except Exception as e:
                    errors['errors'].append({'vote': e.args})

        if collections:
            for collection in collections:
                data = {'user': None,
                        'objects_item': None,
                        'category': [],
                        'image': None,
                        'sync_id': None,
                        'created_at': None,
                        'updated_at': None}

                cl_sync_id = collection.get('sync_id')
                created_at = collection.get('created_at')
                updated_at = collection.get('updated_at')
                ob_sync_id = collection.get('object_sync_id')
                image = collection.get('image')
                ctgrs = collection.get('categories')
                uuid_obj = None

                c_errors = validate_common_fields('collection',
                                                   data,
                                                   Collections,
                                                   clsync_ids,
                                                   entity_sync_id=cl_sync_id,
                                                   created_at=created_at,
                                                   updated_at=updated_at,
                                                   ob_sync_id=ob_sync_id)
                errors['errors'].extend(c_errors)

                if image:
                    try:
                        img_data = base64.b64decode(image)
                        image_buffer = BytesIO(img_data)
                        pil_image = Image.open(image_buffer)
                        image_buffer = BytesIO()
                        pil_image.save(image_buffer, "PNG")
                        img_temp = NamedTemporaryFile(delete=True)
                        img_temp.write(image_buffer.getvalue())
                        img_temp.name = f'/Collections/{str(cl_sync_id)}/image_{cl_sync_id}.jpg'
                        data['image'] = img_temp

                    except:
                        errors['errors'].append({'collection': f'Inappropriate "image" encoding for collection {cl_sync_id} sync_id'})
                else:
                    errors['errors'].append({'collection': f'Value "image" for collection {cl_sync_id} is required'})

                if ctgrs:
                    for cat in ctgrs:
                        try:
                            uuid_obj = uuid.UUID(cat, version=4)
                        except:
                            errors.append({'collection': f'Inappropriate collection sync id {uuid_obj} uuid'})

                        category_object = Categories.objects.filter(sync_id=uuid_obj).first()
                        if category_object:
                            data['category'].append(category_object)
                        else:
                            errors.append({'collection': 'Inappropriate or absent category sync_id'})
                else:
                    errors.append({'collection': 'Sync id for collection category is required'})

                data['user'] = user
                try:
                    ctgs = data.pop('category', None)
                    img = data.pop('image', None)
                    coltn = Collections(**data)
                    coltn.image.save(img.name, img)
                    [coltn.category.add(ctg) for ctg in ctgs]
                    collections_objects.append(coltn)
                except Exception as e:
                    errors['errors'].append({'collection': e.args})

        if len(errors['errors']) > 0:
            return JsonResponse(errors, safe=True)

        table = {'chats': chats_objects, 'votings': votings_objects,
                 'collections': collections_objects}

        for name, lst in table.items():
            for item in lst:
                try:
                    item.save()
                except Exception as e:
                    return JsonResponse({f'{name}': e.args}, safe=True)

        return JsonResponse(serialized_data(museum, settings=settings, categories=categories), safe=True)

