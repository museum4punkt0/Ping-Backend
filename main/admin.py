from django.contrib import admin
from .models import Collections, Users, Settings, Museums, ObjectsItem,\
                    Categories, Categorieslocalizations, ObjectsCategories,\
                    ObjectsImages, Chats, ObjectsImages, MuseumsImages,\
                    ObjectsLocalizations, UsersLanguageStyles, Votings, \
                    PredefinedAvatars

admin.site.site_header = "Museums Admin"
admin.site.site_title = "Museums Admin"


class MuseumsImagesInline(admin.TabularInline):
    model = MuseumsImages
    readonly_fields = ['synced', 'updated_at']


class MuseumsAdmin(admin.ModelAdmin):
    inlines = [MuseumsImagesInline,]
    readonly_fields = ['synced', 'updated_at']


class PredefinedAvatarsInline(admin.TabularInline):
    model = PredefinedAvatars
    readonly_fields = ['synced', 'updated_at']


class SettingsAdmin(admin.ModelAdmin):
    inlines = [PredefinedAvatarsInline,]
    readonly_fields = ['synced', 'updated_at']


class ObjectsImagesInline(admin.TabularInline):
    model = ObjectsImages
    readonly_fields = ['synced', 'updated_at']


class ObjectsLocalizationsInline(admin.TabularInline):
    model = ObjectsLocalizations
    readonly_fields = ['synced', 'updated_at']


class ObjectsItemAdmin(admin.ModelAdmin):
    inlines = [ObjectsImagesInline, ObjectsLocalizationsInline]
    readonly_fields = ['synced', 'updated_at']


class CategorieslocalizationsInline(admin.TabularInline):
    model = Categorieslocalizations
    readonly_fields = ['synced', 'updated_at']


class CategoriesAdmin(admin.ModelAdmin):
    inlines = [CategorieslocalizationsInline]
    readonly_fields = ['synced', 'updated_at']


class UsersLanguageStylesInline(admin.TabularInline):
    model = UsersLanguageStyles
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
admin.site.register(ObjectsCategories)
admin.site.register(Chats)

