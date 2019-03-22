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

