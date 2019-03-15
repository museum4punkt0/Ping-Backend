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
    ObjectslocalizationsSerializer,
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
    serializer_class = ObjectslocalizationsSerializer


@api_view(['GET'])
def synchronise(request):
    """
    Retrieve, update or delete a code snippet.
    """
    # try:
    #     snippet = Snippet.objects.get(pk=pk)
    # except Snippet.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)

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

            museum_images = museum.museumsimages_set.all()
            for image in museum_images:
                image_dict = {}
                serialized_museumsimage =  MuseumsImagesSerializer(instance=image, context=context).data
                image_dict['id'] = serialized_museumsimage['id']
                image_dict['image_type'] = serialized_museumsimage['image_type']
                image_dict['image'] = serialized_museumsimage['image']
                image_dict['sync_id'] = serialized_museumsimage['sync_id']
                image_dict['synced'] = serialized_museumsimage['synced']
                image_dict['created_at'] = serialized_museumsimage['created_at']
                image_dict['updated_at'] = serialized_museumsimage['updated_at']
                museum_table['images'].append(image_dict)

            objects_items = museum.objectsitem_set.all()
            for item in objects_items:
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

                serialized_item = ObjectsItemSerializer(instance=item, context=context).data
                item_table['id'] = serialized_item['id']
                item_table['priority'] = serialized_item['priority']
                item_table['floor'] = serialized_item['floor']
                item_table['positionX'] = serialized_item['positionx']
                item_table['positionY'] = serialized_item['positiony']
                item_table['vip'] = serialized_item['vip']
                item_table['language_style'] = serialized_item['language_style']
                item_table['avatar'] = serialized_item['avatar']
                item_table['onboarding'] = serialized_item['onboarding']
                item_table['sync_id'] = serialized_item['sync_id']
                item_table['synced'] = serialized_item['synced']
                item_table['created_at'] = serialized_item['created_at']
                item_table['updated_at'] = serialized_item['updated_at']

                localizations = item.objectslocalizations_set.all()
                for local in localizations:
                    local_dict = {}
                    serialized_local = ObjectslocalizationsSerializer(instance=local, context=context).data
                    local_dict['id'] = serialized_local['id']
                    local_dict['language'] = serialized_local['language']
                    local_dict['conversation'] = serialized_local['conversation']
                    local_dict['description'] = serialized_local['description']
                    local_dict['title'] = serialized_local['title']
                    local_dict['object_kind'] = serialized_local['object_kind']
                    local_dict['sync_id'] = serialized_local['sync_id']
                    local_dict['synced'] = serialized_local['synced']
                    local_dict['created_at'] = serialized_local['created_at']
                    local_dict['updated_at'] = serialized_local['updated_at']
                    item_table['localizations'].append(local_dict)

                images = item.objectsimages_set.all()
                for image in images:
                    image_dict = {}
                    serialized_image = ObjectsImagesSerializer(instance=image, context=context).data

                    image_dict['id'] = serialized_image['id']
                    image_dict['image'] = serialized_image['image']
                    image_dict['sync_id'] = serialized_image['sync_id']
                    image_dict['synced'] = serialized_image['synced']
                    image_dict['created_at'] = serialized_image['created_at']
                    image_dict['updated_at'] = serialized_image['updated_at']
                    item_table['images'].append(image_dict)
                museum_table['objects'].append(item_table)

            categories = Categories.objects.all()
            for category in categories:
                category_table = {'id': None,
                                 'object_ids': [],
                                 'sync_object_ids': [],
                                 'localizations': [],
                                 'sync_id': None,
                                 'synced': None,
                                 'created_at': None,
                                 'updated_at': None}

                serialized_category = CategoriesSerializer(item).data
                category_table['id'] = serialized_category['id']

                objects = category.objectscategories_set.all()
                category_table['object_ids'] = [{'object_id': i.id} for i in objects]
                category_table['sync_object_ids'] = [{'object_id': i['sync_id']} for i in ObjectsCategoriesSerializer(objects, many=True).data]

                localizations = category.categorieslocalizations_set.all()
                for local in localizations:
                    local_dict = {}
                    serialized_local = CategorieslocalizationsSerializer(local).data
                    local_dict['id'] = serialized_local['id']
                    local_dict['language'] = serialized_local['language']
                    local_dict['title'] = serialized_local['title']
                    local_dict['sync_id'] = serialized_local['sync_id']
                    local_dict['synced'] = serialized_local['synced']
                    local_dict['created_at'] = serialized_local['created_at']
                    local_dict['updated_at'] = serialized_local['updated_at']
                    category_table['localizations'].append(local_dict)

                category_table['sync_id'] = serialized_category['sync_id']
                category_table['synced'] = serialized_category['synced']
                category_table['created_at'] = serialized_category['created_at']
                category_table['updated_at'] = serialized_category['updated_at']
                museum_table['categories'].append(category_table)



            data['museums'] = museum_table
        return JsonResponse(data, safe=True)

    # elif request.method == 'PUT':
    #     serializer = SnippetSerializer(snippet, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == 'DELETE':
    #     snippet.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)