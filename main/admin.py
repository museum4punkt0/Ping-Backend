from django.contrib import admin
from .models import Collections, Users, Settings, Museums, ObjectsItem,\
                    Categories, Categorieslocalizations, ObjectsCategories,\
                    ObjectsImages, Chats, ObjectsImages, MuseumsImages,\
                    ObjectsLocalizations, UsersLanguageStyles, Votings, PredefinedAvatars
# Register your models here.

admin.site.register(Collections)
admin.site.register(Users)
admin.site.register(Settings)
admin.site.register(Museums)
admin.site.register(ObjectsItem)
admin.site.register(Categories)
admin.site.register(Categorieslocalizations)
admin.site.register(ObjectsCategories)
admin.site.register(Chats)
admin.site.register(ObjectsImages)
admin.site.register(MuseumsImages)
admin.site.register(ObjectsLocalizations)
admin.site.register(UsersLanguageStyles)
admin.site.register(Votings)
admin.site.register(PredefinedAvatars)

