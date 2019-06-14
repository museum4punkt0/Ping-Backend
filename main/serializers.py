from django.db.models import F
from rest_framework import serializers
from main.models import (
                     Collections,
                     Users,
                     Settings,
                     Museums,
                     ObjectsItem,
                     Categories,
                     ObjectsCategories,
                     Categorieslocalizations,
                     Chats,
                     ObjectsImages,
                     PredefinedAvatars,
                     MuseumsImages,
                     ObjectsLocalizations,
                     Votings,
                     ObjectsMap,
                     MusemsTensor,
                     DeletedItems,
                     SemanticRelation,
                     SemanticRelationLocalization,
                     OpenningTime,
                     MuseumLocalization
                     )


class SyncObjectField(serializers.RelatedField):
    def to_representation(self, value):
        return '{}'.format(value.sync_id)


class SyncCollectionField(serializers.RelatedField):
    def to_representation(self, value):
        if value.first():
            return '{}'.format(str(value.first().sync_id))


class CollectionsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    objects_item = SyncObjectField(read_only=True)
    category = SyncCollectionField(read_only=True)
    museum_id = serializers.SerializerMethodField()

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

    def get_museum_id(self, obj):
        return obj.objects_item.museum.sync_id


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
        fields = ('id', 'name', 'device_id', 'category', 'positionx',
            'positiony', 'floor', 'language', 'avatar', 'sync_id', 'synced',
            'created_at', 'updated_at', 'chats', 'collections', 'votings')


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
        fields = ('position_score', 'category_score', 'exit_position', 
            'likes_score', 'chat_score', 'priority_score',
            'distance_score', 'predifined_collections', 'languages', 'language_styles', 
            'sync_id', 'synced', 'created_at', 'updated_at', 'predefined_avatars',
            'site_url')


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
        if getattr(value, 'image', None):
            return '{}'.format(value.image.url)


class SemanticRelationLocalizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemanticRelationLocalization
        fields = ('language', 'description', 'created_at', 'updated_at', 'sync_id')


class SemanticRelationSerializer(serializers.Serializer):
    sync_id = serializers.UUIDField()
    object_item_id = serializers.UUIDField()
    localizations = SemanticRelationLocalizationSerializer(many=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class ObjectsItemSerializer(serializers.ModelSerializer):
    images = ObjectsImagesSerializer(many=True)
    localizations = ObjectsLocalizationsSerializer(many=True)
    object_map = ObjectsMapField(read_only=True)
    semantic_relation = serializers.SerializerMethodField()
    museum = serializers.SlugRelatedField(read_only=True, slug_field='sync_id')

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
            'localizations', 'semantic_relation', 'cropped_avatar')

    @staticmethod
    def get_semantic_relation(obj):
        relations_from = SemanticRelation.objects.filter(from_object_item=obj.id)\
            .annotate(object_item_id=F('to_object_item__sync_id'))
        relations_to = SemanticRelation.objects.filter(to_object_item=obj.id)\
            .annotate(object_item_id=F('from_object_item__sync_id'))

        relations_from = SemanticRelationSerializer(relations_from, many=True).data
        relations_to = SemanticRelationSerializer(relations_to, many=True).data

        relations = relations_from + relations_to

        return relations


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
        fields = ('mobile_tensor_flow_model', 'mobile_tensor_flow_lables',
                  'sync_id', 'created_at', 'updated_at')


class OpenningTimeSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(OpenningTimeSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = OpenningTime
        fields = ('weekday', 'from_hour', 'to_hour')


class MuseumLocalizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuseumLocalization
        exclude = ('id', 'museum')


class MuseumsSerializer(serializers.ModelSerializer):
    objectsitems = ObjectsItemSerializer(source='objects_query', many=True)
    museumimages = MuseumsImagesSerializer(many=True)
    museumtensor = MusemsTensorSerializer(many=True)
    opennings = OpenningTimeSerializer()
    localizations = MuseumLocalizationSerializer(many=True)

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
        fields = ('floor_amount', 'settings', 'opennings',
                  'museumtensor',
                  'sync_id', 'synced', 'created_at',
                  'updated_at', 'objectsitems', 'museumimages',
                  'museum_site_url', 'ratio_pixel_meter', 'localizations')


class ShortMuseumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Museums
        fields = ('name', 'sync_id', 'created_at', 'updated_at')


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


class DeletedItemsSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DeletedItemsSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = DeletedItems
        fields = ('__all__')