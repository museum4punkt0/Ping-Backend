import json
import distutils.util
import datetime
import uuid
import base64
from PIL import Image
from io import BytesIO
from collections import defaultdict
from django.core.exceptions import ValidationError
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
    DeletedItems,
    UserTour
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
                                   validate_user,
                                   validate_tours
                                   )
from main.variables import DEFAULT_MUSEUM

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('django')


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
            logger.error(f'User id must be provided')
            return JsonResponse({'error': 'Existing user id must be provided'},
                                safe=True, status=400)
        if museum_id:
            try:
                museum = Museums.objects.get(sync_id=museum_id)
                settings = getattr(museum, 'settings')
            except (Museums.DoesNotExist, ValidationError):
                return JsonResponse({'error': 'Museum not found'}, status=400)
        else:
            logger.error(f'Museum id must be provided')
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
            logger.error('museums settings must be defined')
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
                logger.error(f'User id {user_id} does not exist {e.args}')
                return JsonResponse({'error': f'User id {user_id} does not exist {e.args}'},
                                    safe=True, status=400)
        else:
            logger.error(f'Existing user id must be provided, device id: {user_id}')
            return JsonResponse({'error': 'Existing user id must be provided'},
                                safe=True, status=400)

        try:
            post_data = request.data.get('data')
            if isinstance(post_data, str):
                try:
                    post_data = json.loads(request.data.get('data'))
                except JSONDecodeError:
                    logger.error('Failed loading data to json format')
                    return JsonResponse({'Failed loading datato json format'},
                                        safe=True, status=400)

        except (json.JSONDecodeError, TypeError):
            logger.error('json data with schema {"add": {}, "update": {},"delete": {}, "get": {} } must be transfered')
            return JsonResponse({'error': 'json data with schema {"add": {}, \
                                    "update": {},"delete": {}, "get": {} } must be transfered'},
                                safe=True, status=400)

        if post_data and isinstance(post_data, dict):
            get_values = post_data.get('get')
            add_values = post_data.get('add')
            update_values = post_data.get('update')
        else:
            logger.error('json data with schema {"add": {}, "update": {},"delete": {}, "get": {} } must be transfered')
            return JsonResponse({'error': 'json data with schema {"add": {}, \
                        "update": {},"delete": {}, "get": {} } must be transfered'},
                                safe=True, status=400)
        objects_sync_ids = []
        categories_sync_ids = []

        if museum_id:
            try:
                museum = Museums.objects.get(sync_id=museum_id)
            except (Museums.DoesNotExist, ValidationError):
                logger.error('Museum not found')
                return JsonResponse({'error': 'Museum not found'}, status=400)
        else:
            logger.error(f'Museum id must be provided')
            return JsonResponse(
                {'error': 'Existing museum id must be provided'},
                safe=True, status=400)

        if get_values.get('objects'):
            objects_sync_ids.extend(get_values.get('objects'))

        # traverse 'get' table
        museum.objects_to_serialize = list(set(objects_sync_ids))
        logger.info(f'GET objects to serialize {objects_sync_ids} ')

        if get_values.get('categories'):
            if isinstance(get_values.get('categories'), list):
                categories_sync_ids.extend(get_values.get('categories'))
            else:
                logger.error('Categories must be list')
                return JsonResponse(
                    {'error': 'Categories must be list'},
                    safe=True, status=400)

        logger.info(f'GET objects: {get_values.get("objects")}, \
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
        tours = add_values.get('tours')

        chats_objects = []
        votings_objects = []
        collections_objects = []
        tours_objects = []

        chats_data = []
        votings_data = []
        tours_data = []

        up_chats = update_values.get('chats')
        up_votings = update_values.get('votings')
        up_collections = update_values.get('collections')
        up_tours = update_values.get('tours')
        up_user_data = update_values.get('user')

        logger.info(f'POST chats: {chats}, \
                       POST votings: {votings}, \
                       POST collections: {collections}, \
                       POST collections: {tours}, \
                       POST up_chats: {up_chats}, \
                       POST up_votings: {up_votings}, \
                       POST up_collections: {up_collections}, \
                       POST up_collections: {up_tours}, \
                       POST up_user_data: {up_user_data}')

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
                logger.info(f'POST CHAT \
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
                    logger.error(errors)
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
                    logger.error(errors)                    
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
                image_key = collection.get('image')
                image = request.data.get(image_key)
                ctgrs = collection.get('categories')
                logger.info(f'POST COLLECTION \
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
                    logger.error(errors)
                    return JsonResponse(errors, safe=True)

                try:
                    ctgs = validated_data.pop('category', None)
                    img = validated_data.pop('image', None)
                    coltn = Collections(**validated_data)
                    if img:
                        coltn.image.save(img[1], img[0])
                    [coltn.category.add(ctg) for ctg in ctgs]
                    collections_objects.append(coltn)
                except Exception as e:
                    errors['add_errors'].append({'collection': e.args})

                if len(errors['add_errors']) > 0:
                    return JsonResponse(errors, safe=True, status=400)


        if tours:
            for tour in tours:
                data = {'user': None,
                        'museum_tour': None,
                        'sync_id': None,
                        'created_at': None,
                        'updated_at': None}

                tr_sync_id = tour.get('sync_id')
                created_at = tour.get('created_at')
                updated_at = tour.get('updated_at')
                mus_tr_sync_id = tour.get('museumtour_sync_id')

                validated_data, errors = validate_tours('add',
                                                         data,
                                                         user,
                                                         errors,
                                                         tr_sync_id,
                                                         created_at,
                                                         updated_at,
                                                         mus_tr_sync_id)
                if len(errors['add_errors']) > 0:
                    logger.error(errors)
                    return JsonResponse(errors, safe=True, status=400)
                try:
                    tours_objects.append(UserTour(**validated_data))
                except Exception as e:
                    errors['add_errors'].append({'vote': e.args})

        table = {'chats': chats_objects,
                 'votings': votings_objects,
                 'collections': collections_objects,
                 'tours': tours_objects}

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
                    logger.error(errors)
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
                    logger.error(errors)
                    return JsonResponse(errors, safe=True)

                votings_data.append(validated_data)

        if up_collections:
            """
            Accepts updated collectons serialized data structure. 
                {
                   "add":{},
                   "update":{ 
                      "collections":[ 
                         { 
                            "object_sync_id":"ddab2ad6-67bb-48fa-8f6a-c4c5fe6336e1",
                            "image":"test_avatar",
                            "categories":[ 
                               "66251f34-27fd-4030-8a0a-62eeb9f33090"
                            ],
                            "sync_id":"0da256ef-e389-4ada-8990-73de91411008",
                            "created_at":"2019-03-20T15:15:52.900016Z",
                            "updated_at":"2019-05-20T15:15:52.900049Z"
                         }
                      ]
                   },
                   "delete":{},
                   "get":{}
                }
            """

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
                image_key = collection.get('image')
                image = request.data.get(image_key)
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
                    logger.error(errors)
                    return JsonResponse(errors, safe=True)

                ctgs = validated_data.pop('category', None)
                img = validated_data.pop('image', None)
                coltn = Collections.objects.filter(sync_id=validated_data['sync_id']).first()
                if coltn:
                    try:
                        for (key, value) in validated_data.items():
                            setattr(coltn, key, value)
                        coltn.category.set(ctgs)
                        coltn.save()
                    except Exception as e:
                        errors['update_errors'].append({'collection': e.args})
                        logger.error(errors)
                        return JsonResponse(errors, safe=True)
                    else:
                        try:
                            if img:
                                coltn.image.save(img[1], img[0])
                        except Exception as e:
                            errors['update_errors'].append({'collection': f'collection image update failed: {e.args}'})
                            logger.error(errors)
                            return JsonResponse(errors, safe=True)

        if up_tours:
            for tour in up_tours:
                data = {'user': None,
                        'museum_tour': None,
                        'sync_id': None,
                        'created_at': None,
                        'updated_at': None}

                tr_sync_id = tour.get('sync_id')
                created_at = tour.get('created_at')
                updated_at = tour.get('updated_at')
                mus_tr_sync_id = tour.get('museumtour_sync_id')

                validated_data, errors = validate_tours('update',
                                                         data,
                                                         user,
                                                         errors,
                                                         tr_sync_id,
                                                         created_at,
                                                         updated_at,
                                                         mus_tr_sync_id)
                if len(errors['add_errors']) > 0:
                    logger.error(errors)
                    return JsonResponse(errors, safe=True, status=400)
                try:
                    tours_objects.append(UserTour(**validated_data))
                except Exception as e:
                    errors['add_errors'].append({'vote': e.args})

        table = {'chats': [Chats, chats_data],
                 'votings': [Votings, votings_data],
                 'tours': [UserTour, tours_data]}

        for name, lst in table.items():
            for data in lst[1]:
                try:
                    lst[0].objects.filter(sync_id=data['sync_id']).update(**data)
                except Exception as e:
                    logger.error({f'{name}': e.args})
                    return JsonResponse({f'{name}': e.args}, safe=True)

        if up_user_data:
            """
            Accepts updated users serialized data structure. 
                { 
                   "add":{},
                   "update":{ 
                      "user":{ 
                         "name":"Franky",
                         "positionX":2,
                         "positionY":3,
                         "floor":2,
                         "language":"de",
                         "device_id":"972349236",
                         "avatar":"test_avatar",
                         "language_style":[ 
                            { 
                               "sync_id":"79a54ca0-561c-11e9-a33f-f97d7aa22efe",
                               "score":56,
                               "style":"easy"
                            }
                         ],
                         "sync_id":"14f1134c-cc28-4942-b089-2b18935bce35",
                         "created_at":"2019-03-20T15:15:52.900016Z",
                         "updated_at":"2019-03-20T15:15:52.900049Z"
                      }
                   },
                   "delete":{},
                   "get":{}
                }
            """
            data = {'name': None,
                    'avatar': None,
                    'positionx': None,
                    'positiony': None,
                    'floor': None,
                    'language': None,
                    'language_style': None,
                    'font_size': None,
                    'level': None,
                    'sync_id': None,
                    'created_at': None,
                    'updated_at': None}

            us_sync_id = up_user_data.get('sync_id')
            created_at = up_user_data.get('created_at')
            updated_at = up_user_data.get('updated_at')
            name = up_user_data.get('name')
            avatar_key = up_user_data.get('avatar')
            avatar = request.data.get(avatar_key)
            category = up_user_data.get('category')
            positionx = up_user_data.get('positionX')
            positiony = up_user_data.get('positionY')
            floor = up_user_data.get('floor')
            language = up_user_data.get('language')
            language_style = up_user_data.get('language_style')
            font_size = up_user_data.get('font_size')
            level = up_user_data.get('level')
            score = up_user_data.get('score')
            device_id = up_user_data.get('device_id')

            logger.error(f'!!!!POST USER \
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
                                                    font_size,
                                                    level,
                                                    score,
                                                    device_id)

            if len(errors['update_errors']) > 0:
                logger.error(errors)
                return JsonResponse(errors, safe=True)

            language_style = data.pop('language_style', None)
            avatar = data.pop('avatar', None)
            sync_id = data.pop('sync_id', None)
            language_style.save()
            user = Users.objects.filter(sync_id=sync_id, device_id=user_id).first()
            if not user:
                errors['update_errors'].append({'user': 'User device id and sync id does not match'})
                logger.error(errors)
                return JsonResponse(errors, safe=True)
            else:                    
                try:
                    for (key, value) in validated_data.items():
                        setattr(user, key, value)
                    if avatar:
                        user.avatar.save(avatar[1], avatar[0])
                    user.save()
                except Exception as e:
                    errors['update_errors'].append({'user': e.args})
                    logger.error(errors)
                    return JsonResponse(errors, safe=True)

        return JsonResponse(serialize_synch_data(museum, settings=settings, categories=categories), safe=True)
