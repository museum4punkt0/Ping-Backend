from rest_framework import serializers
from .models import Collections, Users, Settings, Museums, ObjectsItem, \
                    Categories, ObjectsCategories, Categorieslocalizations, Chats, \
                    ObjectsImages, PredefinedAvatars, MuseumsImages, \
                    ObjectsLocalizations, Votings, ObjectsMap, MusemsTensor


class SyncObjectField(serializers.RelatedField):
    def to_representation(self, value):
        return '{}'.format(value.sync_id)


class CollectionsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    objects_item = SyncObjectField(read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(CollectionsSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Collections
        fields = ('__all__')

class ChatsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    objects_item = SyncObjectField(read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(ChatsSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Chats
        fields = ('__all__')


class VotingsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    objects_item = SyncObjectField(read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(VotingsSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Votings
        fields = ('__all__')

class UserCategoryField(serializers.RelatedField):
    def to_representation(self, value):
        return '{}'.format(value.sync_id)

class UsersSerializer(serializers.ModelSerializer):
    chats = ChatsSerializer(many=True)
    collections = CollectionsSerializer(many=True)
    votings = VotingsSerializer(many=True)
    category = UserCategoryField(read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(UsersSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Users
        fields = ('id', 'name', 'device_id', 'category', 'positionx', 'positiony', 
            'floor', 'language', 'avatar', 'sync_id', 'synced', 'created_at', 'updated_at', 'chats', 'collections', 'votings')


class PredefinedAvatarsSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(PredefinedAvatarsSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = PredefinedAvatars
        fields = ('__all__')


class SettingsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    predefined_avatars = PredefinedAvatarsSerializer(many=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(SettingsSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Settings
        fields = ('id', 'position_score', 'category_score', 'exit_position', 
            'likes_score', 'chat_score', 'priority_score',
            'distance_score', 'predifined_collections', 'languages', 'language_styles', 
            'sync_id', 'synced', 'created_at', 'updated_at', 'predefined_avatars')


class ObjectsLocalizationsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(ObjectsLocalizationsSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


    class Meta:
        model = ObjectsLocalizations
        fields = ('__all__')


class ObjectsImagesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(ObjectsImagesSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = ObjectsImages
        fields = ('__all__')


class ObjectsMapField(serializers.RelatedField):

    def to_representation(self, value):
        return '{}'.format(value.image.url)

class ObjectsItemSerializer(serializers.ModelSerializer):
    images = ObjectsImagesSerializer(many=True)
    localizations = ObjectsLocalizationsSerializer(many=True)
    object_map = ObjectsMapField(read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(ObjectsItemSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = ObjectsItem
        fields = ('id', 'priority', 'museum', 'floor', 'positionx', 'positiony', 
            'vip', 'language_style', 'avatar', 'onboarding', 'object_map',
            'sync_id', 'synced', 'created_at', 'updated_at', 'images',
            'localizations')


class MuseumsImagesSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(MuseumsImagesSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = MuseumsImages
        fields = ('__all__')


class MusemsTensorSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(MusemsTensorSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = MusemsTensor
        fields = ('__all__')


class MuseumsSerializer(serializers.ModelSerializer):
    objectsitems = ObjectsItemSerializer(source='objects_query', many=True)
    museumimages = MuseumsImagesSerializer(many=True)
    museumtensor = MusemsTensorSerializer(many=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(MuseumsSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Museums
        fields = ('id', 'name', 'floor_amount', 'settings', 'museumtensor',
                  'sync_id', 'synced', 'created_at',
                  'updated_at', 'objectsitems', 'museumimages')


class CategorieslocalizationsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(CategorieslocalizationsSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Categorieslocalizations
        fields = ('__all__')


class CategoriesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    localizations = CategorieslocalizationsSerializer(many=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(CategoriesSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Categories
        fields = ('__all__')


class ObjectsCategoriesSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(ObjectsCategoriesSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = ObjectsCategories
        fields = ('__all__')

