from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('collections', views.CollectionsView)
router.register('objects', views.ObjectsView)
router.register('chats', views.ChatsView)
router.register('users', views.UsersView)
router.register('museums', views.MuseumsView)
router.register('settings', views.SettingsView)
router.register('objectsimages', views.ObjectsImagesView)
router.register('objectslocalizations', views.ObjectsLocalizationsView)

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
    path('api/v1/synchronise/', views.synchronise),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)