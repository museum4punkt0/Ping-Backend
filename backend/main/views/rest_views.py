from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models import F
from django.http import JsonResponse

from main.variables import MINIMAL_DISTANCE
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
)

from main.serializers import (
    CollectionsSerializer,
    UsersSerializer,
    SettingsSerializer,
    MuseumsSerializer,
    ShortMuseumsSerializer,
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
)


class MuseumsView(viewsets.ReadOnlyModelViewSet):
    queryset = Museums.objects.all()
    serializer_class = ShortMuseumsSerializer

    def list(self, request):
        located_museum = None
        try:
            latitude = float(request.GET.get("lat"))
            longitude = float(request.GET.get("lon"))
            point = Point(longitude, latitude, srid=4326)
        except:
            point = Point()
        if not point.coords:
            museums = Museums.objects.all().order_by("id")
        else:
            museums = Museums.objects.annotate(
                distance=Distance("location", point)
            ).order_by("distance")
            if MINIMAL_DISTANCE:
                located_museum = museums.filter(distance__lte=MINIMAL_DISTANCE)
        serialized = MuseumsSerializer(
            museums,
            fields=(
                "opennings",
                "museumimages",
                "sync_id",
                "created_at",
                "updated_at",
                "museum_site_url",
                "ratio_pixel_meter",
                "localizations",
                "tours",
            ),
            many=True,
        ).data
        located_data = []

        for i in serialized:
            i["located"] = (
                True
                if located_museum and i["sync_id"] == str(located_museum[0].sync_id)
                else False
            )
            located_data.append(i)
        return Response(located_data)
