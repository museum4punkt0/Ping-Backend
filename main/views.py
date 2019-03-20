from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from  django.http import JsonResponse
from .models import (
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

from .serializers import (
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
    ObjectsImagesSerializer
    )



class CollectionsView(viewsets.ModelViewSet):
    queryset = Collections.objects.all()
    serializer_class = CollectionsSerializer


class UsersView(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class SettingsView(viewsets.ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer


class MuseumsView(viewsets.ModelViewSet):
    queryset = Museums.objects.all()
    serializer_class = MuseumsSerializer


class ObjectsView(viewsets.ModelViewSet):
    queryset = ObjectsItem.objects.all()
    serializer_class = ObjectsItemSerializer


class CategoriesView(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class ChatsView(viewsets.ModelViewSet):
    queryset = Chats.objects.all()
    serializer_class = ChatsSerializer


class ObjectsImagesView(viewsets.ModelViewSet):
    queryset = ObjectsImages.objects.all()
    serializer_class = ObjectsImagesSerializer


class MuseumsImagesView(viewsets.ModelViewSet):
    queryset = MuseumsImages.objects.all()
    serializer_class = MuseumsImagesSerializer


class ObjectsLocalizationsView(viewsets.ModelViewSet):
    queryset = ObjectsLocalizations.objects.all()
    serializer_class = ObjectsLocalizationsSerializer


@api_view(['GET'])
def synchronise(request):

    if request.method == 'GET':
        context = {'request': request}
        museums = Museums.objects.all()
        data = {'museums': None,
                'users': None,
                'settings': None}

        for museum in museums:
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

            categories = Categories.objects.all()
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
                category_table['object_ids'] = [{'object_id': i.id} for i in objects]
                category_table['sync_object_ids'] = [{'object_id': i['sync_id']} for i in ObjectsCategoriesSerializer(objects, many=True).data]

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
        return JsonResponse(data, safe=True)

