from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from main.models import (
    Collections,
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
    MusemsTensorSerializer,
    MuseumLocalizationSerializer
    )

from main.variables import DEFAULT_MUSEUM


FETCH_FIELDS = ('sync_id', 'updated_at')

@api_view(['GET'])
def fetch(request):

    if request.method == 'GET':
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
        if museum_id:
            museum = Museums.objects.get(sync_id=museum_id)
            settings = getattr(museum, 'settings')
        else:
            # logging.error(f'Museum id must be provided')
            # return JsonResponse({'error': 'Existing museum id must be provided'},
            #                     safe=True, status=400)
            museum = Museums.objects.get(name=DEFAULT_MUSEUM)
            settings = getattr(museum, 'settings')


        data = {'museums': None,
                'users': None,
                'settings': None,
                'deleted': None}

        s_user = UsersSerializer(user, fields=FETCH_FIELDS).data
        user_table = {'sync_id': None,
                      'updated_at': None,
                      'chats': [],
                      'votings': [],
                      'collections': []}

        user_table['sync_id'] = s_user['sync_id']
        user_table['updated_at'] = s_user['updated_at']

        chats = user.chats_set.all()
        for chat in chats:
            s_chat = ObjectsItemSerializer(chat, fields=FETCH_FIELDS).data
            chat_dict = {}
            chat_dict['sync_id'] = s_chat['sync_id']
            chat_dict['updated_at'] = s_chat['updated_at']
            user_table['chats'].append(chat_dict)

        votings = user.votings_set.all()
        for vote in votings:
            s_vote = ObjectsItemSerializer(vote, fields=FETCH_FIELDS).data
            vote_dict = {}
            vote_dict['sync_id'] = s_vote['sync_id']
            vote_dict['updated_at'] = s_vote['updated_at']
            user_table['votings'].append(vote_dict)

        collections = user.collections_set.all()
        for collection in collections:
            s_collection = ObjectsItemSerializer(collection, fields=FETCH_FIELDS).data
            collection_dict = {}
            collection_dict['sync_id'] = s_collection['sync_id']
            collection_dict['updated_at'] = s_collection['updated_at']
            user_table['collections'].append(collection_dict)

        data['users'] = user_table

        s_museum = MuseumsSerializer(museum, fields=FETCH_FIELDS).data
        museum_table = {'sync_id': None,
                        'updated_at': None,
                        'tensor': [],
                        'images': [],
                        'objects': [],
                        'categories': [],
                        'localizations': []}

        museum_table['sync_id'] = s_museum['sync_id']
        museum_table['updated_at'] = s_museum['updated_at']

        museum_localizations = museum.localizations.all()
        for localizations in museum_localizations:
            localizations = MuseumLocalizationSerializer(localizations, fields=FETCH_FIELDS).data
            museum_table['localizations'].append(localizations)

        tensors = museum.museumtensor.all()
        for tensor in tensors:
            s_image = MuseumsSerializer(tensor, fields=FETCH_FIELDS).data
            tensor_dict = {}
            tensor_dict['sync_id'] = s_image['sync_id']
            tensor_dict['updated_at'] = s_image['updated_at']
            museum_table['tensor'].append(tensor_dict)

        images = museum.museumsimages_set.all()
        for image in images:
            s_image = MuseumsSerializer(image, fields=FETCH_FIELDS).data
            image_dict = {}
            image_dict['sync_id'] = s_image['sync_id']
            image_dict['updated_at'] = s_image['updated_at']
            museum_table['images'].append(image_dict)

        items = museum.objectsitem_set.all()
        for item in items:
            s_item = ObjectsItemSerializer(item, fields=FETCH_FIELDS).data
            item_table = {'sync_id': None,
                          'updated_at': None,
                          'localizations': [],
                          'images': []}

            item_table['sync_id'] = s_item['sync_id']
            item_table['updated_at'] = s_item['updated_at']

            localizations = item.localizations
            for local in localizations:
                s_local = ObjectsItemSerializer(local, fields=FETCH_FIELDS).data
                local_dict = {}
                local_dict['sync_id'] = s_local['sync_id']
                local_dict['updated_at'] = s_local['updated_at']
                item_table['localizations'].append(local_dict)

            images = item.images
            for image in images:
                s_image = ObjectsItemSerializer(image, fields=FETCH_FIELDS).data
                image_dict = {}
                image_dict['sync_id'] = s_image['sync_id']
                image_dict['updated_at'] = s_image['updated_at']
                item_table['images'].append(image_dict)
            museum_table['objects'].append(item_table)

        categories = Categories.objects.all()
        for category in categories:
            s_category = CategoriesSerializer(category, fields=FETCH_FIELDS).data
            category_table = {'localizations': [],
                              'sync_id': None,
                              'updated_at': None}

            localizations = category.localizations
            for local in localizations:
                s_local = CategoriesSerializer(local, fields=FETCH_FIELDS).data
                local_dict = {}
                local_dict['sync_id'] = s_local['sync_id']
                local_dict['updated_at'] = s_local['updated_at']
                category_table['localizations'].append(local_dict)

            category_table['sync_id'] = s_category['sync_id']
            category_table['updated_at'] = s_category['updated_at']
            museum_table['categories'].append(category_table)
        data['museums'] = museum_table

        s_settings = SettingsSerializer(settings, fields=FETCH_FIELDS).data
        settings_table = {'sync_id': None,
                          'updated_at': None}

        settings_table['sync_id'] = s_settings['sync_id']
        settings_table['updated_at'] = s_settings['updated_at']
        data['settings'] = settings_table

        deleted_table = {'objects': None,
                         'categories': None,
                         'updated_at': None}

        del_obj = DeletedItems.objects.filter(category__isnull=True).order_by('-created_at')
        del_cat = DeletedItems.objects.filter(objects_item__isnull=True).order_by('-created_at')

        if del_obj:
            deleted_table['objects'] = [i.objects_item for i in del_obj]
            deleted_table['updated_at'] = del_obj[0].created_at
        if del_cat and del_obj:
            deleted_table['categories'] = [i.category for i in del_cat]
            if del_cat[0].created_at > del_obj[0].created_at:
                deleted_table['updated_at'] = del_cat[0].created_at

        data['deleted'] = deleted_table

        return JsonResponse(data, safe=True)
