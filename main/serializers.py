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
                     MuseumLocalization,
                     MuseumTour,
                     MuseumTourLocalization,
                     TourObjectsItems,
                     UserTour,
                     SuggestedObject,
                     ChatDesigner,
                     SingleLine,
                     SingleLineLocalization
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


class UserTourSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(UserTourSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = UserTour
        fields = ('__all__')


class UserCategoryField(serializers.RelatedField):
    def to_representation(self, value):
        return '{}'.format(value.sync_id)


class UsersSerializer(serializers.ModelSerializer):
    chats = ChatsSerializer(many=True)
    collections = CollectionsSerializer(many=True)
    votings = VotingsSerializer(many=True)
    category = UserCategoryField(read_only=True)
    user_tours = UserTourSerializer(many=True)

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
            'created_at', 'updated_at', 'chats', 'collections', 'votings',
            'user_tours', 'user_level', 'font_size')


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
        fields = ('redirection_timout', 'position_score', 'category_score', 'exit_position', 
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


class SuggestedObjectSerializer(serializers.ModelSerializer):
    sync_id = serializers.CharField(source='suggested.sync_id')

    class Meta:
        model = SuggestedObject
        fields = ('position', 'sync_id')


class SingleLineLocalizationSerializer(serializers.ModelSerializer):
    sync_id = serializers.CharField()
    language = serializers.CharField()
    text = serializers.CharField()

    class Meta:
        model = SingleLineLocalization
        fields = ('sync_id', 'language', 'text')


class RedirectField(serializers.RelatedField):
    def to_representation(self, value):

        return '{}'.format(value.sync_id)


class SingleLineSerializer(serializers.ModelSerializer):
    sync_id = serializers.CharField()
    localizations = SingleLineLocalizationSerializer(source='localization', many=True)
    multichoices = serializers.CharField(source='multichoice')
    redirect = serializers.SerializerMethodField()

    def get_redirect(self, obj):
        redirect= SingleLine.objects.filter(position=obj.redirect)
        if redirect:
            return redirect[0].sync_id

    class Meta:
        model = SingleLine
        fields = ('sync_id', 'position', 'line_type', 'redirect', 'multichoices', 'localizations')


class ChatDesignerSerializer(serializers.ModelSerializer):
    sync_id = serializers.CharField()
    lines = SingleLineSerializer(source='single_line', many=True)

    class Meta:
        model = ChatDesigner
        fields = ('sync_id', 'poll', 'lines')


class ObjectsItemSerializer(serializers.ModelSerializer):
    images = ObjectsImagesSerializer(many=True)
    localizations = ObjectsLocalizationsSerializer(many=True)
    object_map = ObjectsMapField(read_only=True)
    semantic_relation = serializers.SerializerMethodField()
    museum = serializers.SlugRelatedField(read_only=True, slug_field='sync_id')
    objects_to_suggest = SuggestedObjectSerializer(source='sug_objectsitem', many=True)
    chat_objects = ChatDesignerSerializer(source='chat_designer', many=True)

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
            'vip', 'author', 'language_style', 'avatar', 'onboarding', 'object_map', 
            'object_level', 'sync_id', 'synced', 'created_at', 'updated_at', 'images',
            'localizations', 'semantic_relation', 'cropped_avatar', 'objects_to_suggest', 
            'chat_objects')

    @staticmethod
    def get_semantic_relation(obj):
        relations = SemanticRelation.objects.filter(from_object_item=obj.id)\
            .annotate(object_item_id=F('to_object_item__sync_id'))

        return SemanticRelationSerializer(relations, many=True).data


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

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = MuseumLocalization
        exclude = ('id', 'museum')



class TourObjectField(serializers.RelatedField):
    def to_representation(self, value):
        if value.first():
            return [str(i.tour_object.sync_id) for i in  value.all()]


class MuseumTourLocalizationSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = MuseumTourLocalization
        exclude = ('id', 'tour')


class MuseumTourSerializer(serializers.ModelSerializer):
    localizations = MuseumTourLocalizationSerializer(many=True)
    tourobjects = TourObjectField(read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = MuseumTour
        exclude = ('id', 'museum')


class MuseumsSerializer(serializers.ModelSerializer):
    objectsitems = ObjectsItemSerializer(source='objects_query', many=True)
    museumimages = MuseumsImagesSerializer(many=True)
    museumtensor = MusemsTensorSerializer(many=True)
    opennings = OpenningTimeSerializer()
    localizations = MuseumLocalizationSerializer(many=True)
    tours = MuseumTourSerializer(many=True)

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
                  'museum_site_url', 'ratio_pixel_meter', 'localizations',
                  'tours')


class ShortMuseumsSerializer(serializers.ModelSerializer):
    localizations = MuseumLocalizationSerializer(many=True)

    class Meta:
        model = Museums
        fields = ('sync_id', 'created_at', 'updated_at',
                  'localizations')


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


def serialize_synch_data(museum,
                    user=None,
                    settings=None,
                    categories=None,
                    foreign_museums=None):

    data = {'museums': None,
            'users': None,
            'settings': None,
            'deleted': None,
            'foreign_objects': None}

    # museum serialization
    serialized_museum = MuseumsSerializer(museum).data

    museum_table = {'sync_id': None,
                    'floor_amount': None,
                    'opennings': None,
                    'museum_site_url': None,
                    'ratio_pixel_meter': None,
                    'tensor': [],
                    'images': [],
                    'objects': [],
                    'categories': [],
                    'localizations': [],
                    'tours': []}

    museum_table['sync_id'] = serialized_museum['sync_id']
    museum_table['floor_amount'] = serialized_museum['floor_amount']
    museum_table['opennings'] = serialized_museum['opennings']
    museum_table['museum_site_url'] = serialized_museum['museum_site_url']
    museum_table['ratio_pixel_meter'] = serialized_museum['ratio_pixel_meter']
    museum_table['localizations'] = serialized_museum['localizations']

    serialized_museumtensor = serialized_museum['museumtensor']
    for tensor in serialized_museumtensor:
        tensor_dict = {}
        tensor_dict['tensor_flow_model'] = tensor['mobile_tensor_flow_model']
        tensor_dict['tensor_flow_lables'] = tensor['mobile_tensor_flow_lables']
        tensor_dict['sync_id'] = tensor['sync_id']
        tensor_dict['created_at'] = tensor['created_at']
        tensor_dict['updated_at'] = tensor['updated_at']

        museum_table['tensor'].append(tensor_dict)


    serialized_museumsimages = serialized_museum['museumimages']
    for image in serialized_museumsimages:
        image_dict = {}
        image_dict['id'] = image['id']
        image_dict['image_type'] = image['image_type']
        image_dict['image'] = image['image']
        image_dict['sync_id'] = image['sync_id']
        image_dict['created_at'] = image['created_at']
        image_dict['updated_at'] = image['updated_at']
        museum_table['images'].append(image_dict)

    serialized_tours = serialized_museum['tours']
    for tour in serialized_tours:
        tour_table = {'tourobjects': [],
                      'localizations': [],
                      'sync_id': None,
                      'created_at': None,
                      'updated_at': None}

        localizations = tour['localizations']
        for local in localizations:
            local_dict = {}
            local_dict['language'] = local['language']
            local_dict['title'] = local['title']
            local_dict['description'] = local['description']
            local_dict['sync_id'] = local['sync_id']
            local_dict['created_at'] = local['created_at']
            local_dict['updated_at'] = local['updated_at']
            tour_table['localizations'].append(local_dict)

        tour_table['tourobjects'] = tour['tourobjects']
        tour_table['sync_id'] = tour['sync_id']
        tour_table['created_at'] = tour['created_at']
        tour_table['updated_at'] = tour['updated_at']
        museum_table['tours'].append(tour_table)

    # objectsitems serialilzation
    serialized_objects_items = serialized_museum['objectsitems']
    for item in serialized_objects_items:
        item_table = {'id': None,
                      'priority': None,
                      'floor': None,
                      'positionX': None,
                      'positionY': None,
                      'vip': None,
                      'author': None,
                      'language_style': None,
                      'avatar': None,
                      'cropped_avatar': None,
                      'onboarding': None,
                      'object_map': None,
                      'level': None,
                      'sync_id': None,
                      'created_at': None,
                      'updated_at': None,
                      'localizations': [],
                      'images': [],
                      'semantic_relations': [],
                      'objects_to_suggest': [],
                      'chat_objects': []}

        item_table['id'] = item['id']
        item_table['priority'] = item['priority']
        item_table['floor'] = item['floor']
        item_table['positionX'] = item['positionx']
        item_table['positionY'] = item['positiony']
        item_table['vip'] = item['vip']
        item_table['author'] = item['author']
        item_table['language_style'] = item['language_style']
        item_table['avatar'] = item['avatar']
        item_table['cropped_avatar'] = item['cropped_avatar']
        item_table['onboarding'] = item['onboarding']
        item_table['object_map'] = item['object_map']
        item_table['level'] = int(item['object_level'])
        item_table['sync_id'] = item['sync_id']
        item_table['created_at'] = item['created_at']
        item_table['updated_at'] = item['updated_at']
        item_table['semantic_relations'] = item['semantic_relation']
        item_table['objects_to_suggest'] = item['objects_to_suggest']
        item_table['chat_objects'] = item['chat_objects']


        localizations = item['localizations']
        for local in localizations:
            local_dict = {}
            local_dict['id'] = local['id']
            local_dict['language'] = local['language']
            local_dict['conversation'] = local['conversation']
            local_dict['phrase'] = local['phrase']
            local_dict['description'] = local['description']
            local_dict['title'] = local['title']
            local_dict['object_kind'] = local['object_kind']
            local_dict['sync_id'] = local['sync_id']
            local_dict['created_at'] = local['created_at']
            local_dict['updated_at'] = local['updated_at']
            item_table['localizations'].append(local_dict)

        serialized_images = item['images']
        for image in serialized_images:
            image_dict = {}
            image_dict['id'] = image['id']
            image_dict['number'] = image['number']
            image_dict['image'] = image['image']
            image_dict['sync_id'] = image['sync_id']
            image_dict['created_at'] = image['created_at']
            image_dict['updated_at'] = image['updated_at']
            item_table['images'].append(image_dict)
        museum_table['objects'].append(item_table)

    # categories serialization
    for category in categories:
        serialized_category = CategoriesSerializer(category).data
        category_table = {'id': None,
                          'sync_object_ids': [],
                          'localizations': [],
                          'sync_id': None,
                          'created_at': None,
                          'updated_at': None}

        category_table['id'] = serialized_category['id']

        # objects = category.objectscategories_set.filter(objects_item__museum=museum)
        objects = category.objectscategories_set.all()
        category_table['sync_object_ids'] = [str(i.objects_item.sync_id) for i in objects]

        localizations = serialized_category['localizations']
        for local in localizations:
            local_dict = {}
            local_dict['id'] = local['id']
            local_dict['language'] = local['language']
            local_dict['title'] = local['title']
            local_dict['sync_id'] = local['sync_id']
            local_dict['created_at'] = local['created_at']
            local_dict['updated_at'] = local['updated_at']
            local_dict['description'] = local['description']
            category_table['localizations'].append(local_dict)

        category_table['sync_id'] = serialized_category['sync_id']
        category_table['created_at'] = serialized_category['created_at']
        category_table['updated_at'] = serialized_category['updated_at']
        museum_table['categories'].append(category_table)

    data['museums'] = museum_table

    # user serialization
    if user:
        serialized_user = UsersSerializer(user).data
        user_table = {'id': None,
                      'name': None,
                      'avatar': None,
                      'category': None,
                      'positionX': None,
                      'positionY': None,
                      'floor': None,
                      'language': None,
                      'language_style': None,
                      'score': None,
                      'level': None,
                      'font_size': None,
                      'sync_id': None,
                      'created_at': None,
                      'updated_at': None,
                      'chats': [],
                      'votings': [],
                      'collections': [],
                      'tours': []
                      }

        user_table['id'] = serialized_user['id']
        user_table['name'] = serialized_user['name']
        user_table['avatar'] = serialized_user['avatar']
        user_table['category'] = serialized_user['category']
        user_table['positionX'] = serialized_user['positionx']
        user_table['positionY'] = serialized_user['positiony']
        user_table['floor'] = serialized_user['floor']
        user_table['language'] = serialized_user['language']
        uls = getattr(user, 'userslanguagestyles', None)
        language_style = getattr(uls, 'language_style', None)
        score = getattr(uls, 'score', None)
        user_table['language_style'] = language_style
        user_table['score'] = score
        user_table['level'] = int(serialized_user['user_level'])
        user_table['font_size'] = serialized_user['font_size']
        user_table['sync_id'] = serialized_user['sync_id']
        user_table['created_at'] = serialized_user['created_at']
        user_table['updated_at'] = serialized_user['updated_at']

        serialized_chats = serialized_user['chats']
        for chat in serialized_chats:
            chat_dict = {}
            chat_dict['id'] = chat['id']
            chat_dict['object_id'] = chat['objects_item']
            chat_dict['last_step'] = chat['last_step']
            chat_dict['finished'] = chat['finished']
            chat_dict['history'] = chat['history']
            chat_dict['planned'] = chat['planned']
            chat_dict['sync_id'] = chat['sync_id']
            chat_dict['created_at'] = chat['created_at']
            chat_dict['updated_at'] = chat['updated_at']
            user_table['chats'].append(chat_dict)

        serialized_votings = serialized_user['votings']
        for vote in serialized_votings:
            vote_dict = {}
            vote_dict['id'] = vote['id']
            vote_dict['object_id'] = vote['objects_item']
            vote_dict['vote'] = vote['vote']
            vote_dict['sync_id'] = vote['sync_id']
            vote_dict['created_at'] = vote['created_at']
            vote_dict['updated_at'] = vote['updated_at']
            user_table['votings'].append(vote_dict)

        serialized_collections = serialized_user['collections']
        for collection in serialized_collections:
            collection_dict = {}
            collection_dict['object_id'] = collection['objects_item']
            collection_dict['image'] = collection['image']
            collection_dict['category_id'] = collection['category']
            collection_dict['sync_id'] = collection['sync_id']
            collection_dict['created_at'] = collection['created_at']
            collection_dict['updated_at'] = collection['updated_at']
            collection_dict['museum_id'] = collection['museum_id']
            user_table['collections'].append(collection_dict)

        serialized_tours = serialized_user['user_tours']
        for tour in serialized_tours:
            tour_dict = {}
            tour_dict['museumtour_sync_id'] = tour['museum_tour']
            tour_dict['sync_id'] = tour['sync_id']
            tour_dict['created_at'] = tour['created_at']
            tour_dict['updated_at'] = tour['updated_at']
            user_table['tours'].append(tour_dict)
        data['users'] = user_table
    else:
        data['users'] = None

    # settings serialization
    if settings:
        serialized_settings = SettingsSerializer(settings).data
        settings_table = {'id': None,
                          'redirection_timout': None,
                          'position_scores': None,
                          'category_score': None,
                          'exit_position': None,
                          'likes_scores': None,
                          'chat_scores': None,
                          'predifined_objects': [],
                          'priority_scores': None,
                          'distance_scores': None,
                          'predefined_categories': None,
                          'predefined_avatars': None,
                          'languages': [],
                          'language_styles': [],
                          'sync_id': None,
                          'created_at': None,
                          'updated_at': None,
                          'site_url': None}

        settings_table['redirection_timout'] = serialized_settings['redirection_timout']
        settings_table['position_scores'] = serialized_settings['position_score']
        settings_table['category_score'] = serialized_settings['category_score']
        settings_table['exit_position'] = serialized_settings['exit_position']
        settings_table['likes_scores'] = serialized_settings['likes_score']
        settings_table['chat_scores'] = serialized_settings['chat_score']
        settings_table['predifined_objects'] = [str(i.predefined_object.sync_id) for i in settings.settingspredefinedobjectsitems_set.all()]
        settings_table['priority_scores'] = serialized_settings['priority_score']
        settings_table['distance_scores'] = serialized_settings['distance_score']
        settings_table['predefined_avatars'] = [i['image'] for i in serialized_settings['predefined_avatars']]
        settings_table['languages'] = serialized_settings['languages']
        settings_table['language_styles'] = serialized_settings['language_styles']
        settings_table['sync_id'] = serialized_settings['sync_id']
        settings_table['created_at'] = serialized_settings['created_at']
        settings_table['updated_at'] = serialized_settings['updated_at']
        settings_table['site_url'] = serialized_settings['site_url']
        data['settings'] = settings_table
    else:
        data['settings'] = None

    f_objects = []
    if foreign_museums:
        for f_mus in foreign_museums:
            serialized_museum = MuseumsSerializer(f_mus).data
            f_objects.append(serialized_museum['objectsitems'])

    data['foreign_objects'] = f_objects

    deleted_table = {}
    del_obj = DeletedItems.objects.all().order_by('-created_at')
    if del_obj:
        deleted_table['updated_at'] = del_obj[0].created_at

    data['deleted'] = deleted_table

    return data