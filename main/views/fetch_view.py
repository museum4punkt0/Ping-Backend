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

        serialized_user = UsersSerializer(user).data
        user_table = {'sync_id': None,
                      'synced': None,
                      'created_at': None,
                      'updated_at': None,
                      'chats': [],
                      'votings': [],
                      'collections': []
                      }

        user_table['sync_id'] = serialized_user['sync_id']
        user_table['synced'] = serialized_user['synced']
        user_table['created_at'] = serialized_user['created_at']
        user_table['updated_at'] = serialized_user['updated_at']

        serialized_chats = serialized_user['chats']
        for chat in serialized_chats:
            chat_dict = {}
            chat_dict['sync_id'] = chat['sync_id']
            chat_dict['synced'] = chat['synced']
            chat_dict['created_at'] = chat['created_at']
            chat_dict['updated_at'] = chat['updated_at']
            user_table['chats'].append(chat_dict)

        serialized_votings = serialized_user['votings']
        for vote in serialized_votings:
            vote_dict = {}
            vote_dict['sync_id'] = vote['sync_id']
            vote_dict['synced'] = vote['synced']
            vote_dict['created_at'] = vote['created_at']
            vote_dict['updated_at'] = vote['updated_at']
            user_table['votings'].append(vote_dict)

        serialized_collections = serialized_user['collections']
        for collection in serialized_collections:
            collection_dict = {}
            collection_dict['sync_id'] = collection['sync_id']
            collection_dict['synced'] = collection['synced']
            collection_dict['created_at'] = collection['created_at']
            collection_dict['updated_at'] = collection['updated_at']
            user_table['collections'].append(collection_dict)

        data['users'] = user_table

        serialized_museum = MuseumsSerializer(museum).data
        museum_table = {'sync_id': None,
                        'synced': None,
                        'created_at': None,
                        'updated_at': None,
                        'images': [],
                        'objects': [],
                        'categories': []}

        museum_table['sync_id'] = serialized_museum['sync_id']
        museum_table['synced'] = serialized_museum['synced']
        museum_table['created_at'] = serialized_museum['created_at']
        museum_table['updated_at'] = serialized_museum['updated_at']

        serialized_museumsimages = serialized_museum['museumimages']
        for image in serialized_museumsimages:
            image_dict = {}
            image_dict['sync_id'] = image['sync_id']
            image_dict['synced'] = image['synced']
            image_dict['created_at'] = image['created_at']
            image_dict['updated_at'] = image['updated_at']
            museum_table['images'].append(image_dict)

        serialized_objects_items = serialized_museum['objectsitems']
        for item in serialized_objects_items:
            item_table = {'sync_id': None,
                          'synced': None,
                          'created_at': None,
                          'updated_at': None,
                          'localizations': [],
                          'images': []}

            item_table['sync_id'] = item['sync_id']
            item_table['synced'] = item['synced']
            item_table['created_at'] = item['created_at']
            item_table['updated_at'] = item['updated_at']

            localizations = item['localizations']
            for local in localizations:
                local_dict = {}
                local_dict['sync_id'] = local['sync_id']
                local_dict['synced'] = local['synced']
                local_dict['created_at'] = local['created_at']
                local_dict['updated_at'] = local['updated_at']
                item_table['localizations'].append(local_dict)

            serialized_images = item['images']
            for image in serialized_images:
                image_dict = {}
                image_dict['sync_id'] = image['sync_id']
                image_dict['synced'] = image['synced']
                image_dict['created_at'] = image['created_at']
                image_dict['updated_at'] = image['updated_at']
                item_table['images'].append(image_dict)
            museum_table['objects'].append(item_table)

        categories = Categories.objects.all()
        for category in categories:
            serialized_category = CategoriesSerializer(category).data
            category_table = {'localizations': [],
                              'sync_id': None,
                              'synced': None,
                              'created_at': None,
                              'updated_at': None}

            localizations = serialized_category['localizations']
            for local in localizations:
                local_dict = {}
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

        serialized_settings = SettingsSerializer(settings).data
        settings_table = {'sync_id': None,
                          'synced': None,
                          'created_at': None,
                          'updated_at': None}

        settings_table['sync_id'] = serialized_settings['sync_id']
        settings_table['synced'] = serialized_settings['synced']
        settings_table['created_at'] = serialized_settings['created_at']
        settings_table['updated_at'] = serialized_settings['updated_at']
        data['settings'] = settings_table

        return JsonResponse(data, safe=True)
