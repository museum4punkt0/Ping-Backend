import distutils.util
import datetime
import uuid
import base64
from PIL import Image
from io import BytesIO
from collections import defaultdict
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
    ObjectsImages,
    DeletedItems
)
import logging

from main.serializers import (
    serialize_synch_data,
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
    UsersSerializer,
    DeletedItemsSerializer
    )
from main.views.validators import (validate_chats,
                                   validate_votings,
                                   validate_collections,
                                   validate_user
                                   )
from main.variables import DEFAULT_MUSEUM

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.ERROR)


class Synchronization(APIView):

    def get(self, request, format=None):
        user_id = request.GET.get('user_id', None)
        museum_id = request.GET.get('museum_id', None)
        user = None

        if user_id:
            try:
                user = Users.objects.get(device_id=user_id)
            except:
                user = Users.objects.create(device_id=user_id)
        else:
            logging.error(f'User id must be provided')
            return JsonResponse({'error': 'Existing user id must be provided'},
                                safe=True, status=400)
        if museum_id:
            museum = Museums.objects.get(sync_id=museum_id)
            settings = getattr(museum, 'settings')
            serialized_museum = MuseumsSerializer(museum).data
        else:
            logging.error(f'Museum id must be provided')
            return JsonResponse({'error': 'Existing museum id must be provided'},
                                safe=True, status=400)
        foreign_colns = user.collections_set.exclude(objects_item__in=museum.objectsitem_set.all())
        foreign_chats = user.chats_set.exclude(objects_item__in=museum.objectsitem_set.all())
        foreign_objects = [i.objects_item for i in foreign_colns]
        foreign_objects.extend([i.objects_item for i in foreign_chats])
        foreign_museums = list(set([i.museum for i in foreign_objects]))
        mus_obj_table = defaultdict(list)
        for mus in foreign_museums:
            for obj in foreign_objects:
                if obj in mus.objectsitem_set.all():
                    mus_obj_table[mus].append(obj)

        f_musems_to_serialize = []
        for mus, objects in mus_obj_table.items():
            mus.objects_to_serialize = list(set([str(i.sync_id) for i in objects]))
            f_musems_to_serialize.append(mus)

        categories = Categories.objects.all()

        if not settings:
          return JsonResponse({'error': 'museums settings must be defined'},
                              safe=True, status=400)

        return JsonResponse(serialize_synch_data(museum, user, settings,
                                categories, f_musems_to_serialize), safe=True)

    def post(self, request, format=None):
        user_id = request.GET.get('user_id', None)
        museum_id = request.GET.get('museum_id', None)
        if user_id:
            try:
                user = Users.objects.get(device_id=user_id)
            except Exception as e:
                logging.error(f'User id {user_id} does not exist {e.args}')
                return JsonResponse({'error': f'User id {user_id} does not exist {e.args}'},
                                    safe=True, status=400)
        else:
            logging.error(f'Existing user id must be provided, device id: {user_id}')
            return JsonResponse({'error': 'Existing user id must be provided'},
                                safe=True, status=400)

        post_data = request.data
        if post_data:
            get_values = post_data.get('get')
            add_values = post_data.get('add')
            update_values = post_data.get('update')
        else:
            return JsonResponse({'error': 'json data with schema {"add": {}, \
                        "update": {},"delete": {}, "get": {} } must be transfered'},
                                safe=True, status=400)
        objects_sync_ids = []
        categories_sync_ids = []

        if museum_id:
            museum = Museums.objects.get(sync_id=museum_id)
        else:
            # logging.error(f'Museum id must be provided')
            # return JsonResponse({'error': 'Existing museum id must be provided'},
            #                     safe=True, status=400)
            museum = Museums.objects.get(name=DEFAULT_MUSEUM)

        if get_values.get('objects'):
            objects_sync_ids.extend(get_values.get('objects'))

        # traverse 'get' table
        museum.objects_to_serialize = list(set(objects_sync_ids))
        logging.info(f'GET objects to serialize {objects_sync_ids} ')

        if get_values.get('categories'):
            if isinstance(get_values.get('categories'), list):
                categories_sync_ids.extend(get_values.get('categories'))
            else:
                return JsonResponse(
                    {'error': 'Categories must be list'},
                    safe=True, status=400)

        logging.info(f'GET objects: {get_values.get("objects")}, \
                      object_images: {get_values.get("object_images")}, \
                      object_localizations: {get_values.get("object_localizations")}, \
                      categories{get_values.get("categories")}, \
                      category_localizations: {get_values.get("category_localizations")}')

        categories = Categories.objects.filter(sync_id__in=categories_sync_ids)

        settings = None
        if get_values.get('settings'):
            settings = Settings.objects.get(sync_id__in=get_values.get('settings'))

        # traverse 'add' values
        errors = {'add_errors': [], 'update_errors': []}

        chats = add_values.get('chats')
        votings = add_values.get('votings')
        collections = add_values.get('collections')

        chats_objects = []
        votings_objects = []
        collections_objects = []

        chats_data = []
        votings_data = []

        up_chats = update_values.get('chats')
        up_votings = update_values.get('votings')
        up_collections = update_values.get('collections')
        up_user_data = update_values.get('user')


        if chats:
            for chat in chats:
                data = {'user': None,
                        'objects_item': None,
                        'finished': None,
                        'history': None,
                        'planned': None,
                        'last_step': None,
                        'sync_id': None,
                        'created_at': None,
                        'updated_at': None}

                ch_sync_id = chat.get('sync_id')
                created_at = chat.get('created_at')
                updated_at = chat.get('updated_at')
                ob_sync_id = chat.get('object_sync_id')
                finished = chat.get('finished')
                history = chat.get('history')
                planned = chat.get('planned')
                last_step = chat.get('last_step')
                logging.info(f'POST CHAT \
                    ch_sync_id: {ch_sync_id, type(ch_sync_id)}, \
                    created_at: {created_at, type(created_at)}, \
                    updated_at: {updated_at, type(updated_at)}, \
                    ob_sync_id{ob_sync_id, type(ob_sync_id)}, \
                    finished: {finished, type(finished)}')

                validated_data, errors = validate_chats('add',
                                                         data,
                                                         user,
                                                         errors,
                                                         ch_sync_id,
                                                         created_at,
                                                         updated_at,
                                                         ob_sync_id,
                                                         finished,
                                                         planned,
                                                         history,
                                                         last_step)

                if len(errors['add_errors']) > 0:
                    return JsonResponse(errors, safe=True, status=400)

                try:
                    chats_objects.append(Chats(**validated_data))
                except Exception as e:
                    errors['add_errors'].append({'chat': e.args})

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

                validated_data, errors = validate_votings('add',
                                                           data,
                                                           user,
                                                           errors,
                                                           vt_sync_id,
                                                           created_at,
                                                           updated_at,
                                                           ob_sync_id,
                                                           vote)

                if len(errors['add_errors']) > 0:
                    return JsonResponse(errors, safe=True, status=400)

                try:
                    votings_objects.append(Votings(**validated_data))
                except Exception as e:
                    errors['add_errors'].append({'vote': e.args})

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
                logging.info(f'POST COLLECTION \
                     ch_sync_id: {cl_sync_id, type(cl_sync_id)}, \
                     created_at: {created_at, type(created_at)}, \
                     updated_at: {updated_at, type(updated_at)}, \
                     ob_sync_id{ob_sync_id, type(ob_sync_id)}, \
                     image: {type(image)}, category {ctgrs, type(ctgrs)}')

                validated_data, errors = validate_collections('add',
                                                               data,
                                                               user,
                                                               errors,
                                                               cl_sync_id,
                                                               created_at,
                                                               updated_at,
                                                               ob_sync_id,
                                                               image,
                                                               ctgrs)

                if len(errors['add_errors']) > 0:
                    return JsonResponse(errors, safe=True)

                try:
                    ctgs = validated_data.pop('category', None)
                    img = validated_data.pop('image', None)
                    coltn = Collections(**validated_data)
                    coltn.image.save(img.name, img)
                    [coltn.category.add(ctg) for ctg in ctgs]
                    collections_objects.append(coltn)
                except Exception as e:
                    errors['add_errors'].append({'collection': e.args})

                if len(errors['add_errors']) > 0:
                    return JsonResponse(errors, safe=True, status=400)

        table = {'chats': chats_objects, 'votings': votings_objects,
                 'collections': collections_objects}

        for name, lst in table.items():
            for item in lst:
                try:
                    item.save()
                except Exception as e:
                    return JsonResponse({f'{name}': e.args}, safe=True,
                                        status=400)

        if up_chats:
            for chat in up_chats:
                data = {'user': None,
                        'objects_item': None,
                        'finished': None,
                        'history': None,
                        'planned': None,
                        'last_step': None,
                        'sync_id': None,
                        'created_at': None,
                        'updated_at': None}
                ch_sync_id = chat.get('sync_id')
                created_at = chat.get('created_at')
                updated_at = chat.get('updated_at')
                ob_sync_id = chat.get('object_sync_id')
                finished = chat.get('finished')
                history = chat.get('history')
                planned = chat.get('planned')
                last_step = chat.get('last_step')


                validated_data, errors = validate_chats('update',
                                                         data,
                                                         user,
                                                         errors,
                                                         ch_sync_id,
                                                         created_at,
                                                         updated_at,
                                                         ob_sync_id,
                                                         finished,
                                                         planned,
                                                         history,
                                                         last_step)

                if len(errors['update_errors']) > 0:
                    return JsonResponse(errors, safe=True)

                chats_data.append(validated_data)

        if up_votings:
            for voting in up_votings:
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

                validated_data, errors = validate_votings('update',
                                                           data,
                                                           user,
                                                           errors,
                                                           vt_sync_id,
                                                           created_at,
                                                           updated_at,
                                                           ob_sync_id,
                                                           vote)

                if len(errors['update_errors']) > 0:
                    return JsonResponse(errors, safe=True)

                votings_data.append(validated_data)

        if up_collections:
            for collection in up_collections:
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

                validated_data, errors = validate_collections('update',
                                                               data,
                                                               user,
                                                               errors,
                                                               cl_sync_id,
                                                               created_at,
                                                               updated_at,
                                                               ob_sync_id,
                                                               image,
                                                               ctgrs)

                if len(errors['update_errors']) > 0:
                    return JsonResponse(errors, safe=True)

                ctgs = validated_data.pop('category', None)
                img = validated_data.pop('image', None)
                coltn = Collections.objects.filter(sync_id=validated_data['sync_id']).first()
                if coltn:
                    try:
                        Collections.objects.filter(sync_id=validated_data['sync_id']).update(**validated_data)
                        coltn.image.save(img.name, img)
                        coltn.category.set(ctgs)
                    except Exception as e:
                        errors['update_errors'].append({'collection': e.args})
                        return JsonResponse(errors, safe=True)

        table = {'chats': [Chats, chats_data],
                 'votings': [Votings, votings_data]}

        for name, lst in table.items():
            for data in lst[1]:
                try:
                    lst[0].objects.filter(sync_id=data['sync_id']).update(**data)
                except Exception as e:
                    return JsonResponse({f'{name}': e.args}, safe=True)

        if up_user_data:
            data = {'name': None,
                    'avatar': None,
                    'positionx': None,
                    'positiony': None,
                    'floor': None,
                    'language': None,
                    'sync_id': None,
                    'created_at': None,
                    'updated_at': None}

            us_sync_id = up_user_data.get('sync_id')
            created_at = up_user_data.get('created_at')
            updated_at = up_user_data.get('updated_at')
            name = up_user_data.get('name')
            avatar = up_user_data.get('avatar')
            category = up_user_data.get('category')
            positionx = up_user_data.get('positionX')
            positiony = up_user_data.get('positionY')
            floor = up_user_data.get('floor')
            language = up_user_data.get('language')
            language_style = up_user_data.get('language_style')
            score = up_user_data.get('score')
            device_id = up_user_data.get('device_id')

            logging.error(f'!!!!POST USER \
                us_sync_id: {us_sync_id, type(us_sync_id)}, \
                created_at: {created_at, type(created_at)}, updated_at: {updated_at, type(updated_at)}, \
                us_sync_id{us_sync_id, type(us_sync_id)}, floor: {floor, type(floor)}, \
                category {category, type(category)}, language: {language, type(language)}, \
                language_style: {language_style, type(language_style)}, \
                score: {score, type(score)}')

            validated_data, errors = validate_user('update',
                                                    data,
                                                    user,
                                                    errors,
                                                    us_sync_id,
                                                    created_at,
                                                    updated_at,
                                                    name,
                                                    avatar,
                                                    category,
                                                    positionx,
                                                    positiony,
                                                    floor,
                                                    language,
                                                    language_style,
                                                    score,
                                                    device_id)

            if len(errors['update_errors']) > 0:
                return JsonResponse(errors, safe=True)

            language_style = data.pop('language_style', None)
            avatar = data.pop('avatar', None)
            sync_id = data.pop('sync_id', None)
            language_style.save()
            if avatar:
                user.avatar.save(avatar.name, avatar)

            try:
                if not Users.objects.filter(sync_id=sync_id, device_id=user_id).update(**data):
                    errors['update_errors'].append({'user': 'User device id and sync id does not match'})
                    return JsonResponse(errors, safe=True)
            except Exception as e:
                errors['update_errors'].append({'user': e.args})
                return JsonResponse(errors, safe=True)

        return JsonResponse(serialize_synch_data(museum, settings=settings, categories=categories), safe=True)
