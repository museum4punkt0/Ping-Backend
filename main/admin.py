from django.contrib import admin
from .models import Collections, Users, Settings, Museums, ObjectsItem,\
                    Categories, Categorieslocalizations, ObjectsCategories,\
                    ObjectsImages, Chats, ObjectsImages, MuseumsImages,\
                    ObjectsLocalizations, UsersLanguageStyles, Votings, \
                    PredefinedAvatars
from mein_objekt.settings import NUMBER_OF_LOCALIZATIONS

admin.site.site_header = "Museums Admin"
admin.site.site_title = "Museums Admin"

class MinValidatedInlineMixIn:
    validate_min = True
    def get_formset(self, *args, **kwargs):
        return super().get_formset(validate_min=self.validate_min, *args, **kwargs)


class PredefinedAvatarsInline(admin.TabularInline):
    model = PredefinedAvatars
    readonly_fields = ['synced', 'updated_at']


class SettingsAdmin(admin.ModelAdmin):
    inlines = [PredefinedAvatarsInline,]
    readonly_fields = ['synced', 'updated_at']


class MuseumsImagesInline(admin.TabularInline):
    model = MuseumsImages
    readonly_fields = ['synced', 'updated_at']


class MuseumsAdmin(admin.ModelAdmin):
    inlines = [MuseumsImagesInline,]
    readonly_fields = ['synced', 'updated_at']


class ObjectsImagesInline(admin.TabularInline):
    model = ObjectsImages
    extra = 0
    readonly_fields = ['synced', 'updated_at']


class ObjectsLocalizationsInline(MinValidatedInlineMixIn, admin.TabularInline):
    model = ObjectsLocalizations
    min_num = NUMBER_OF_LOCALIZATIONS
    extra = 0
    readonly_fields = ['synced', 'updated_at']


class ObjectsCategoriesInline(MinValidatedInlineMixIn, admin.TabularInline):
    model = ObjectsCategories
    min_num = 1
    extra = 0
    readonly_fields = ['synced', 'updated_at']


class ObjectsItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_title', 'museum', 'onboarding', 'vip', 'updated_at')
    inlines = [ObjectsLocalizationsInline, ObjectsImagesInline, ObjectsCategoriesInline]
    readonly_fields = ['synced', 'updated_at']

    # def get_queryset(self, request):
    #     return super(ObjectsItemAdmin,self).get_queryset(request).select_related('objectslocalizations_set')

    def get_title(self, obj):
        obj = obj.objectslocalizations_set.first()
        title = getattr(obj, 'title', None)
        if title:
            return title
        else:
            return 'No title'


class CategorieslocalizationsInline(MinValidatedInlineMixIn, admin.TabularInline):
    model = Categorieslocalizations
    min_num = NUMBER_OF_LOCALIZATIONS
    extra = 0
    readonly_fields = ['synced', 'updated_at']


class CategoriesAdmin(admin.ModelAdmin):
    inlines = [CategorieslocalizationsInline]
    readonly_fields = ['synced', 'updated_at']


class UsersLanguageStylesInline(MinValidatedInlineMixIn, admin.TabularInline):
    model = UsersLanguageStyles
    min_num = NUMBER_OF_LOCALIZATIONS
    extra = 0
    readonly_fields = ['synced', 'updated_at']


class VotingsInline(admin.TabularInline):
    model = Votings
    readonly_fields = ['synced', 'updated_at', 'objects_item', 'vote']


class UsersAdmin(admin.ModelAdmin):
    inlines = [UsersLanguageStylesInline, VotingsInline]
    readonly_fields = ['synced', 'updated_at']


admin.site.register(Collections)
admin.site.register(Users, UsersAdmin)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(Museums, MuseumsAdmin)
admin.site.register(ObjectsItem, ObjectsItemAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Chats)

