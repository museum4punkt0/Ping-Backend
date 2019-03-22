from django.contrib import admin
from django.urls import path, include
from main.views import fetch_view, rest_views, synch_view
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('collections', rest_views.CollectionsView)
router.register('objects', rest_views.ObjectsView)
router.register('chats', rest_views.ChatsView)
router.register('users', rest_views.UsersView)
router.register('museums', rest_views.MuseumsView)
router.register('settings', rest_views.SettingsView)
router.register('objectsimages', rest_views.ObjectsImagesView)
router.register('objectslocalizations', rest_views.ObjectsLocalizationsView)

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
    path('api/v1/synchronise/', synch_view.synchronise),
    path('api/v1/fetch/', fetch_view.fetch),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)