from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Collections, Users, Settings, Museums, ObjectsItem,\
                    Categories, Categorieslocalizations, ObjectsCategories,\
                    ObjectsImages, Chats, ObjectsImages, MuseumsImages,\
                    ObjectsLocalizations, UsersLanguageStyles, Votings, \
                    PredefinedAvatars, SettingsPredefinedObjectsItems, \
                    ObjectsMap, MusemsTensor
from mein_objekt.settings import NUMBER_OF_LOCALIZATIONS

admin.site.site_header = "Museums Admin"
admin.site.site_title = "Museums Admin"
from django.forms.models import BaseInlineFormSet


class MinValidatedInlineMixIn:
    validate_min = True
    def get_formset(self, *args, **kwargs):
        return super().get_formset(validate_min=self.validate_min, *args, **kwargs)


class PredefinedAvatarsInline(MinValidatedInlineMixIn, admin.TabularInline):
    model = PredefinedAvatars
    min_num = 0 # should be 6
    extra = 0
    readonly_fields = ['updated_at']
    exclude = ('synced',)


class SettingsPredefinedObjectsItemsInline(MinValidatedInlineMixIn, admin.TabularInline):
    model = SettingsPredefinedObjectsItems
    min_num = 8
    extra = 0
    readonly_fields = ['updated_at']
    exclude = ('synced',)


class SettingsAdmin(admin.ModelAdmin):
    inlines = [PredefinedAvatarsInline, SettingsPredefinedObjectsItemsInline]
    readonly_fields = ['updated_at']
    exclude = ('synced',)


class MusImagesFormSet(BaseInlineFormSet):
   def clean(self):
        super(MusImagesFormSet, self).clean()

        mus_image_types = [i.instance.image_type for i in self.forms]
        map_types = [True for i in mus_image_types if 'map' in i]
        pointer_types = [True for i in mus_image_types if 'pnt' in i]
        if not any(map_types):
            raise ValidationError('There must be at least one map image with type "<floor_number>_map"!')
        if len(pointer_types) != 1:
            raise ValidationError('There must be exatly one pointer image with type "pnt"!')


class MuseumsImagesInline(admin.TabularInline):
    model = MuseumsImages
    min_number = 2
    extra = 0
    readonly_fields = ['updated_at']
    exclude = ('synced',)
    formset = MusImagesFormSet


class MusemsTensorInline(admin.TabularInline):
    model = MusemsTensor
    min_number = 2
    extra = 0
    readonly_fields = ['updated_at']
    exclude = ('synced',)


class MuseumsAdmin(admin.ModelAdmin):
    inlines = [MusemsTensorInline, MuseumsImagesInline,]
    readonly_fields = ['updated_at']
    exclude = ('synced',)


class ObjectsImagesInline(admin.TabularInline):
    model = ObjectsImages
    extra = 0
    readonly_fields = ['updated_at']
    exclude = ('synced',)


class ObjectsLocalizationsInline(MinValidatedInlineMixIn, admin.TabularInline):
    model = ObjectsLocalizations
    min_num = NUMBER_OF_LOCALIZATIONS
    extra = 0
    readonly_fields = ['updated_at']
    exclude = ('synced',)


class ObjectsCategoriesInline(MinValidatedInlineMixIn, admin.TabularInline):
    model = ObjectsCategories
    min_num = 1
    extra = 0
    readonly_fields = ['updated_at']
    exclude = ('synced',)


class ObjectsMapAdmin(admin.ModelAdmin):
    list_display = ('thumbnail',)


class ObjectsMapInline(admin.TabularInline):
    model = ObjectsMap
    extra = 0
    fields = ('thumbnail',)
    readonly_fields = ['thumbnail']
    exclude = ('synced',)


class ObjectsItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'avatar_id', 'museum', 'onboarding', 'vip',
                    'updated_at', 'categories')
    inlines = [ObjectsLocalizationsInline, ObjectsImagesInline,
               ObjectsCategoriesInline, ObjectsMapInline]
    readonly_fields = ['updated_at']
    exclude = ('synced',)

    # def get_queryset(self, request):
    #     return super(ObjectsItemAdmin,self).get_queryset(request).select_related('objectslocalizations_set')

    def avatar_id(self, obj):
        avatar = getattr(obj, 'avatar', None)
        if avatar:
            return avatar.name.split('/')[-1][:20]


    def title(self, obj):
        obj = obj.objectslocalizations_set.first()
        title = getattr(obj, 'title', None)
        if title:
            return title

    def categories(self, obj):
        obj_cat = getattr(obj, 'objectscategories', None)
        if obj_cat:
            categories = obj_cat.category.all()
            if categories:
                return [i.id for i in categories]


class CategorieslocalizationsInline(MinValidatedInlineMixIn, admin.TabularInline):
    model = Categorieslocalizations
    min_num = NUMBER_OF_LOCALIZATIONS
    extra = 0
    readonly_fields = ['updated_at']
    exclude = ('synced',)


class CategoriesAdmin(admin.ModelAdmin):
    inlines = [CategorieslocalizationsInline]
    readonly_fields = ['updated_at']
    exclude = ('synced',)


class UsersLanguageStylesInline(MinValidatedInlineMixIn, admin.TabularInline):
    model = UsersLanguageStyles
    min_num = NUMBER_OF_LOCALIZATIONS
    extra = 0
    readonly_fields = ['language_style', 'score', 'updated_at']
    exclude = ('synced',)


class VotingsInline(admin.TabularInline):
    model = Votings
    extra = 0
    readonly_fields = ['objects_item', 'vote', 'updated_at', 'sync_id']
    fields = ('objects_item', 'vote', 'updated_at', 'sync_id', )
    exclude = ('synced',)


class CollectionsInline(admin.TabularInline):
    model = Collections
    extra = 0
    readonly_fields = ['objects_item', 'category', 'image', 'updated_at', 'sync_id']
    fields = ('objects_item', 'category', 'image', 'updated_at', 'sync_id', )
    exclude = ('synced',)


class ChatsInline(admin.TabularInline):
    model = Chats
    extra = 0
    readonly_fields = ['objects_item', 'last_step', 'history', 'finished', 'updated_at', 'sync_id']
    fields = ('objects_item', 'last_step', 'history', 'finished', 'updated_at', 'sync_id')
    exclude = ('synced',)


class UsersAdmin(admin.ModelAdmin):
    inlines = [UsersLanguageStylesInline, VotingsInline, CollectionsInline,
               ChatsInline]
    readonly_fields = ['name', 'avatar', 'device_id', 'category', 'positionx', 'positiony', 'floor', 'language', 'updated_at']
    exclude = ('synced',)


class VotingsAdmin(admin.ModelAdmin):
    model = Votings
    readonly_fields = ['updated_at']
    exclude = ('synced',)


admin.site.register(Users, UsersAdmin)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(Museums, MuseumsAdmin)
admin.site.register(ObjectsItem, ObjectsItemAdmin)
admin.site.register(Categories, CategoriesAdmin)
