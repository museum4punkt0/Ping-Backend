from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.gis.db import models
from mapwidgets.widgets import GooglePointFieldWidget
from .models import Collections, Users, Settings, Museums, ObjectsItem,\
                    Categories, Categorieslocalizations, ObjectsCategories,\
                    ObjectsImages, Chats, ObjectsImages, MuseumsImages,\
                    ObjectsLocalizations, UsersLanguageStyles, Votings, \
                    PredefinedAvatars, SettingsPredefinedObjectsItems, \
                    ObjectsMap, MusemsTensor, SemanticRelationLocalization, \
                    SemanticRelation, OpenningTime, MuseumLocalization
from main.variables import NUMBER_OF_LOCALIZATIONS

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
        logo_types = [True for i in mus_image_types if 'logo' in i]

        if not any(map_types):
            raise ValidationError('There must be at least one map image with type "<floor_number>_map"!')
        if len(pointer_types) != 1:
            raise ValidationError('There must be exatly one pointer image with type "pnt"!')
        if len(logo_types) != 1:
            raise ValidationError('There must be one image with type "logo"!')


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


class MusemsOpeningInline(admin.TabularInline):
    model = OpenningTime
    min_number = 1
    extra = 0


class MuseumLocalizationInline(admin.TabularInline):
    readonly_fields = ['updated_at']
    model = MuseumLocalization
    extra = 0


class MuseumsAdmin(admin.ModelAdmin):
    inlines = [MuseumLocalizationInline, MusemsOpeningInline,
               MusemsTensorInline, MuseumsImagesInline]
    readonly_fields = ['updated_at']
    exclude = ('synced',)
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }


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


class SemanticRelatedLocalizationInline(admin.TabularInline):
    readonly_fields = ['updated_at']
    model = SemanticRelationLocalization
    extra = 0


class SemanticRelationForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        to_object_item = cleaned_data.get('to_object_item')
        from_object_item = self.cleaned_data.get('from_object_item')

        if to_object_item and from_object_item:

            if to_object_item == from_object_item:
                raise forms.ValidationError(
                    'Semantic relation to self impossible')

            if not self.instance.id:
                relations1 = SemanticRelation.objects.filter(
                    to_object_item=to_object_item,
                    from_object_item=from_object_item).exists()
                relations2 = SemanticRelation.objects.filter(
                    to_object_item=from_object_item,
                    from_object_item=to_object_item).exists()

                if relations1 or relations2:
                    raise forms.ValidationError(
                        'This semantic relation already exists')

        return cleaned_data


class SemanticRelationAdmin(admin.ModelAdmin):
    readonly_fields = ['updated_at']
    model = SemanticRelation
    inlines = [SemanticRelatedLocalizationInline]
    form = SemanticRelationForm


class ObjectsItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'avatar_id', 'chat_id', 'museum',
                    'onboarding', 'vip', 'cropped_avatar',
                    'updated_at', 'categories', 'localizations',
                    'images_number', 'sync_id')
    inlines = [ObjectsLocalizationsInline, ObjectsImagesInline,
               ObjectsCategoriesInline, ObjectsMapInline]
    readonly_fields = ['updated_at']
    exclude = ('synced',)
    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'object_map', None):
            messages.add_message(request, messages.INFO, 'For objects Map been \
                autocreated you should add Museum Map for every museum floor \
                and a pointer image with corresponding image type')
        super(ObjectsItemAdmin, self).save_model(request, obj, form, change)

    # def get_queryset(self, request):
    #     return super(ObjectsItemAdmin,self).get_queryset(request).select_related('objectslocalizations_set')

    def avatar_id(self, obj):
        avatar = getattr(obj, 'avatar', None)
        if avatar:
            return avatar.name.split('/')[-1][:20]

    def chat_id(self, obj):
        obj_loc = getattr(obj, 'objectslocalizations_set', None)
        if obj_loc:
            return [i.conversation.name.split('/')[-1][:20] for i in obj_loc.all()]

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

    def localizations(self, obj):
        obj_loc = getattr(obj, 'objectslocalizations_set', None)
        if obj_loc:
            localizations = obj_loc.all()
            if localizations:
                return [i.language for i in localizations]

    def images_number(self, obj):
        return obj.objectsimages_set.count()


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
    list_display = ['name', 'device_id']
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
admin.site.register(SemanticRelation, SemanticRelationAdmin)
