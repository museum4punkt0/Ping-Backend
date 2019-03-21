from rest_framework import serializers
from .models import Collections, Users, Settings, Museums, ObjectsItem, \
                    Categories, ObjectsCategories, Categorieslocalizations, Chats, \
                    ObjectsImages, PredefinedAvatars, MuseumsImages, \
                    ObjectsLocalizations, Votings


class CollectionsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Collections
        fields = ('__all__')


class ChatsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Chats
        fields = ('__all__')


class VotingsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Votings
        fields = ('__all__')


class UsersSerializer(serializers.ModelSerializer):
    chats = ChatsSerializer(many=True)
    collections = CollectionsSerializer(many=True)
    votings = VotingsSerializer(many=True)

    class Meta:
        model = Users
        fields = ('id', 'name', 'device_id', 'category', 'positionx', 'positiony', 
            'floor', 'language', 'avatar', 'sync_id', 'synced', 'created_at', 'updated_at', 'chats', 'collections', 'votings')


class PredefinedAvatarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredefinedAvatars
        fields = ('__all__')


class SettingsSerializer(serializers.ModelSerializer):
    predefined_avatars = PredefinedAvatarsSerializer(many=True)

    class Meta:
        model = Settings
        fields = ('id', 'position_score', 'category_score', 'exit_position', 
            'likes_score', 'chat_score', 'priority_score',
             'distance_score', 'predifined_collections', 'languages', 'sync_id', 'synced', 'created_at', 'updated_at', 'predefined_avatars')


class ObjectsLocalizationsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = ObjectsLocalizations
        fields = ('__all__')


class ObjectsImagesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = ObjectsImages
        fields = ('__all__')


class ObjectsItemSerializer(serializers.ModelSerializer):
    images = ObjectsImagesSerializer(many=True)
    localizations = ObjectsLocalizationsSerializer(many=True)

    class Meta:
        model = ObjectsItem
        fields = ('id', 'priority', 'museum', 'floor', 'positionx', 'positiony', 
            'vip', 'language_style', 'avatar', 'onboarding', 'sync_id', 
            'synced', 'created_at', 'updated_at', 'images', 'localizations')


class MuseumsImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuseumsImages
        fields = ('__all__')


class MuseumsSerializer(serializers.ModelSerializer):
    objectsitems = ObjectsItemSerializer(many=True)
    museumimages = MuseumsImagesSerializer(many=True)

    class Meta:
        model = Museums
        fields = ('id', 'name', 'floor_amount', 'settings', 'tensor_flow_model', 
            'tensor_flow_lables', 'sync_id', 'synced', 'created_at',
            'updated_at', 'objectsitems', 'museumimages')


class CategorieslocalizationsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Categorieslocalizations
        fields = ('__all__')


class CategoriesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    localizations = CategorieslocalizationsSerializer(many=True)

    class Meta:
        model = Categories
        fields = ('__all__')


class ObjectsCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectsCategories
        fields = ('__all__')

