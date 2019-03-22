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
    ObjectsImages
)

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

from mein_objekt.settings import DEFAULT_MUSEUM
FETCH_FIELDS = ('sync_id', 'synced', 'created_at', 'updated_at')
@api_view(['GET'])
def fetch(request):

    if request.method == 'GET':
        user_id = request.GET.get('user_id', None)
        if user_id:
            user = Users.objects.get(device_id=user_id)
        else:
            return JsonResponse({'error': 'user id must be passed'}, safe=True)

        museum = Museums.objects.get(name=DEFAULT_MUSEUM)
        settings = museum.settings
        data = {'museums': None,
                'users': None,
                'settings': None}

        s_user = UsersSerializer(user, fields=FETCH_FIELDS).data
        user_table = {'sync_id': None,
                      'synced': None,
                      'created_at': None,
                      'updated_at': None,
                      'chats': [],
                      'votings': [],
                      'collections': []}

        user_table['sync_id'] = s_user['sync_id']
        user_table['synced'] = s_user['synced']
        user_table['created_at'] = s_user['created_at']
        user_table['updated_at'] = s_user['updated_at']

        chats = user.chats_set.all()
        for chat in chats:
            s_chat = ObjectsItemSerializer(chat, fields=FETCH_FIELDS).data
            chat_dict = {}
            chat_dict['sync_id'] = s_chat['sync_id']
            chat_dict['synced'] = s_chat['synced']
            chat_dict['created_at'] = s_chat['created_at']
            chat_dict['updated_at'] = s_chat['updated_at']
            user_table['chats'].append(chat_dict)

        votings = user.votings_set.all()
        for vote in votings:
            s_vote = ObjectsItemSerializer(vote, fields=FETCH_FIELDS).data
            vote_dict = {}
            vote_dict['sync_id'] = s_vote['sync_id']
            vote_dict['synced'] = s_vote['synced']
            vote_dict['created_at'] = s_vote['created_at']
            vote_dict['updated_at'] = s_vote['updated_at']
            user_table['votings'].append(vote_dict)

        collections = user.collections_set.all()
        for collection in collections:
            s_collection = ObjectsItemSerializer(collection, fields=FETCH_FIELDS).data
            collection_dict = {}
            collection_dict['sync_id'] = s_collection['sync_id']
            collection_dict['synced'] = s_collection['synced']
            collection_dict['created_at'] = s_collection['created_at']
            collection_dict['updated_at'] = s_collection['updated_at']
            user_table['collections'].append(collection_dict)

        data['users'] = user_table

        s_museum = MuseumsSerializer(museum, fields=FETCH_FIELDS).data
        museum_table = {'sync_id': None,
                        'synced': None,
                        'created_at': None,
                        'updated_at': None,
                        'images': [],
                        'objects': [],
                        'categories': []}

        museum_table['sync_id'] = s_museum['sync_id']
        museum_table['synced'] = s_museum['synced']
        museum_table['created_at'] = s_museum['created_at']
        museum_table['updated_at'] = s_museum['updated_at']

        images = museum.museumsimages_set.all()
        for image in images:
            s_image = MuseumsSerializer(image, fields=FETCH_FIELDS).data
            image_dict = {}
            image_dict['sync_id'] = s_image['sync_id']
            image_dict['synced'] = s_image['synced']
            image_dict['created_at'] = s_image['created_at']
            image_dict['updated_at'] = s_image['updated_at']
            museum_table['images'].append(image_dict)

        items = museum.objectsitem_set.all()
        for item in items:
            s_item = ObjectsItemSerializer(item, fields=FETCH_FIELDS).data
            item_table = {'s_sync_id': None,
                          'synced': None,
                          'created_at': None,
                          'updated_at': None,
                          'localizations': [],
                          'images': []}

            item_table['sync_id'] = s_item['sync_id']
            item_table['synced'] = s_item['synced']
            item_table['created_at'] = s_item['created_at']
            item_table['updated_at'] = s_item['updated_at']

            localizations = item.localizations
            for local in localizations:
                s_local = ObjectsItemSerializer(local, fields=FETCH_FIELDS).data
                local_dict = {}
                local_dict['sync_id'] = s_local['sync_id']
                local_dict['synced'] = s_local['synced']
                local_dict['created_at'] = s_local['created_at']
                local_dict['updated_at'] = s_local['updated_at']
                item_table['localizations'].append(local_dict)

            images = item.images
            for image in images:
                s_image = ObjectsItemSerializer(image, fields=FETCH_FIELDS).data
                image_dict = {}
                image_dict['sync_id'] = s_image['sync_id']
                image_dict['synced'] = s_image['synced']
                image_dict['created_at'] = s_image['created_at']
                image_dict['updated_at'] = s_image['updated_at']
                item_table['images'].append(image_dict)
            museum_table['objects'].append(item_table)

        categories = Categories.objects.all()
        for category in categories:
            s_category = CategoriesSerializer(category, fields=FETCH_FIELDS).data
            category_table = {'localizations': [],
                              'sync_id': None,
                              'synced': None,
                              'created_at': None,
                              'updated_at': None}

            localizations = category.localizations
            for local in localizations:
                s_local = CategoriesSerializer(local, fields=FETCH_FIELDS).data
                local_dict = {}
                local_dict['sync_id'] = s_local['sync_id']
                local_dict['synced'] = s_local['synced']
                local_dict['created_at'] = s_local['created_at']
                local_dict['updated_at'] = s_local['updated_at']
                category_table['localizations'].append(local_dict)

            category_table['sync_id'] = s_category['sync_id']
            category_table['synced'] = s_category['synced']
            category_table['created_at'] = s_category['created_at']
            category_table['updated_at'] = s_category['updated_at']
            museum_table['categories'].append(category_table)
        data['museums'] = museum_table

        s_settings = SettingsSerializer(settings, fields=FETCH_FIELDS).data
        settings_table = {'sync_id': None,
                          'synced': None,
                          'created_at': None,
                          'updated_at': None}

        settings_table['sync_id'] = s_settings['sync_id']
        settings_table['synced'] = s_settings['synced']
        settings_table['created_at'] = s_settings['created_at']
        settings_table['updated_at'] = s_settings['updated_at']
        data['settings'] = settings_table

        return JsonResponse(data, safe=True)
