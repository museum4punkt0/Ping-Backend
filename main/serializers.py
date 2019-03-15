from rest_framework import serializers
from .models import Collections, Users, Settings, Museums, ObjectsItem, \
                    Categories, ObjectsCategories, Categorieslocalizations, Chats, \
                    ObjectsImages, PredefinedAvatars, MuseumsImages, ObjectsLocalizations

class CollectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collections
        fields = ('id', 'user', 'objects_item', 'image', 'url', 'sync_id', 'synced', 'created_at', 'updated_at')


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'name', 'device_id', 'category', 'positionx', 'positiony', 
            'floor', 'language', 'avatar', 'sync_id', 'synced', 'created_at', 'updated_at')

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ('id', 'position_score', 'category_score', 'exit_position', 
            'likes_score', 'chat_score', 'predifined_objects', 'priority_score',
             'distance_score', 'predifined_collections', 'languages', 'sync_id', 'synced', 'created_at', 'updated_at')


class MuseumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Museums
        fields = ('id', 'name', 'floor_amount', 'settings', 'tensor_flow_model', 
            'tensor_flow_lables', 'sync_id', 'synced', 'created_at', 'updated_at')


class ObjectsItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ObjectsItem
        fields = ('id', 'priority', 'museum', 'floor', 'positionx', 'positiony', 
            'vip', 'language_style', 'avatar', 'onboarding', 'sync_id', 'synced', 'created_at', 'updated_at')


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('__all__')


class CategorieslocalizationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorieslocalizations
        fields = ('__all__')


class ObjectslocalizationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectsLocalizations
        fields = ('__all__')


class ObjectsCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectsCategories
        fields = ('__all__')


class ChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chats
        fields = ('__all__')


class ObjectsImagesSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = ObjectsImages
        fields = ('__all__')


class PredefinedAvatarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredefinedAvatars
        fields = ('__all__')


class MuseumsImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuseumsImages
        fields = ('__all__')