from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from django.core.files.temp import NamedTemporaryFile
from django.utils.html import format_html
from types import MethodType
from model_utils import Choices
import urllib
import uuid
import os
from PIL import Image
from io import BytesIO
from mein_objekt.settings import DEFAULT_MUSEUM
from multiselectfield import MultiSelectField

LANGUEAGE_STYLE_CHOICES = Choices(
        ('easy', 'Easy'),
        ('fun', 'Fun'),
        ('kids', 'Kids'),
        ('professional', 'Professional')
      )

PRIORITY_CHOICES = Choices(
        (1, 'first', 'First'),
        (2, 'second', 'Second'),
        (3, 'third', 'Third'),
        (4, 'fourth', 'Fourth'),
        (5, 'fifth', 'Fifth')
      )

LOCALIZATIONS_CHOICES = Choices(
        ('en', 'English'),
        ('de', 'German'),
      )

DEFAULT_MUSEUM_SETTINGS = {
        "position_score": "{1: 5, 2: 3}",
        "exit_position": "{1: 5, 2: 3}",
        "likes_score": "{1: 5, 2: 3}",
        "chat_score": "{1: 5, 2: 3}",
        "priority_score": "{1: 5, 2: 3}",
        "distance_score": "{1: 5, 2: 3}",
        "predifined_collections": "{1: 5, 2: 3}",
        "languages": "{1: 5, 2: 3}",
        "synced": False,
    }

IMAGE_TYPES = Choices(
        ('smpl', 'Simple'),
        ('pnt', 'Pointer'),
        ('1_map', 'First floor map'),
        ('2_map', 'Second floor map'),
        ('3_map', 'Third floor map'),
      )

def get_image_path(instance, filename):
    syncid = getattr(instance, 'sync_id', None).urn.split(':')[-1]
    if instance.__class__.__name__ in ('Users', 'Collections'):
        dir_name = f'User/{syncid}'
        if instance.__class__.__name__ == 'Collections':
            user_syncid = instance.user.sync_id.urn.split(':')[-1]
            dir_name = f'User/{user_syncid}/Collection'
    elif instance.__class__.__name__ in ('ObjectsItem',
        'MuseumsImages', 'ObjectsImages', 'PredefinedAvatars', 'ObjectsLocalizations'):
        object_syncid = instance.sync_id
        museum_name = getattr(instance, 'museum', None)
        if museum_name is None:
            item = getattr(instance, 'objects_item', None)
            if item:
                museum_name = getattr(item, 'museum', None).name
                object_syncid = getattr(item, 'sync_id', None)
        dir_name = f'Museum/{museum_name}'
        if instance.__class__.__name__ == 'MuseumsImages':
            museum_name = instance.museum
        if instance.__class__.__name__ in ('ObjectsItem', 'ObjectsImages', 'ObjectsLocalizations'):
            dir_name += f'/Objects/{object_syncid}'
        if instance.__class__.__name__ == 'PredefinedAvatars':
            dir_name = f'Museum/PredefinedAvatars'
    return os.path.join('images', dir_name, filename)


class Users(models.Model):
    class Meta:
        verbose_name_plural = "Users"

    id = models.AutoField(primary_key=True, serialize=True, verbose_name='ID')
    name = models.CharField(max_length=45, blank=True, null=True)
    avatar = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    device_id = models.CharField(max_length=45, blank=True, null=True)
    category = models.CharField(max_length=45, blank=True, null=True)
    positionx = models.DecimalField(db_column='positionX', max_digits=11, decimal_places=8)
    positiony = models.DecimalField(db_column='positionY', max_digits=11, decimal_places=8)
    floor = models.IntegerField()
    language = models.CharField(max_length=45, choices=LOCALIZATIONS_CHOICES, default=LOCALIZATIONS_CHOICES.en)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    @property
    def chats(self):
        return self.chats_set.all()

    @property
    def collections(self):
        return self.collections_set.all()

    @property
    def votings(self):
        return self.votings_set.all()


    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Users, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}: {self.name}'


class Categories(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    @property
    def localizations(self):
        return self.categorieslocalizations_set.all()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Categories, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'


class Settings(models.Model):
    class Meta:
        verbose_name_plural = "Settings"

    position_score = JSONField(default=list)
    category_score = JSONField(blank=True, null=True)
    exit_position = JSONField()
    likes_score = JSONField()
    chat_score = JSONField()
    priority_score = JSONField(default=list)
    distance_score = JSONField()
    predifined_collections = JSONField()
    predefined_categories = models.ManyToManyField(Categories)
    languages = MultiSelectField(choices=LOCALIZATIONS_CHOICES,
                                 max_choices=2,
                                 max_length=20)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    # collections = models.ForeignKey(Collection, models.DO_NOTHING)

    @property
    def predefined_avatars(self):
        return self.predefinedavatars_set.all()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Settings, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'


class PredefinedAvatars(models.Model):
    class Meta:
        verbose_name_plural = "Predefined Avatars"

    image = models.ImageField(upload_to=get_image_path, blank=True, null=True, max_length=110)
    settings = models.ForeignKey(Settings, models.CASCADE, blank=True, null=True)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(PredefinedAvatars, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'


class Museums(models.Model):
    class Meta:
        verbose_name_plural = "Museums"

    name = models.CharField(max_length=45, unique=True, default=DEFAULT_MUSEUM)
    floor_amount = models.IntegerField()
    settings = models.ForeignKey(Settings, models.SET_NULL, null=True)
    tensor_flow_model = models.CharField(max_length=45, blank=True, null=True)
    tensor_flow_lables = models.CharField(max_length=45, blank=True, null=True)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    _objects_to_serialize = None

    @property
    def objects_to_serialize(self):
        return self._objects_to_serialize

    @objects_to_serialize.setter
    def objects_to_serialize(self, x):
        self._objects_to_serialize = x

    def objects_query(self):
        if self.objects_to_serialize is not None:
            return ObjectsItem.objects.filter(sync_id__in=self._objects_to_serialize)
        else:
            return ObjectsItem.objects.all()

    @property
    def objectsitems(self):
        return self.objectsitem_set.all()

    @property
    def museumimages(self):
        return self.museumsimages_set.all()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Museums, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class ObjectsItem(models.Model): 
    class Meta:
        verbose_name_plural = "Objects"

    priority = models.IntegerField(choices=PRIORITY_CHOICES,
        default=PRIORITY_CHOICES.first)
    museum = models.ForeignKey(Museums, models.PROTECT)
    floor = models.IntegerField()
    positionx = models.DecimalField(db_column='positionX', max_digits=3, decimal_places=0)
    positiony = models.DecimalField(db_column='positionY', max_digits=3, decimal_places=0)
    vip = models.BooleanField(default=False)
    language_style = models.CharField(max_length=45, choices=LANGUEAGE_STYLE_CHOICES, default='easy')
    avatar = models.ImageField(upload_to=get_image_path, blank=True, null=True, max_length=110)
    onboarding = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    @property
    def images(self):
        return self.objectsimages_set.all()

    @property
    def localizations(self):
        return self.objectslocalizations_set.all()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        museum = self.museum
        mus_map = museum.museumsimages_set.filter(image_type=f'{self.floor}_map')
        mus_pointer = museum.museumsimages_set.filter(image_type='pnt')
        if mus_map and mus_pointer:
            if getattr(mus_map[0], 'image', None) and \
               getattr(mus_pointer[0], 'image', None):
                mus_response = urllib.request.urlopen(mus_map[0].image.url).read()
                pnt_response = urllib.request.urlopen(mus_pointer[0].image.url).read()

                if mus_response and pnt_response:
                    mus_io = BytesIO(mus_response)
                    pnt_io = BytesIO(pnt_response)

                    mus_image = Image.open(mus_io)
                    pnt_image = Image.open(pnt_io)
                    mask = Image.new('L', (30, 30), 100)

                    pnt_image = pnt_image.resize((30, 30))
                    mus_image.paste(pnt_image, (int(self.positionx), int(self.positiony)), mask=mask)
                    # final = Image.alpha_composite(m)

                    image_buffer = BytesIO()
                    mus_image.save(image_buffer, "PNG")

                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(image_buffer.getvalue())

                    if getattr(self, 'object_map', None):
                        self.object_map.delete()
                    om = ObjectsMap()
                    om.objects_item = self
                    om.image.save(f'/o_maps/{str(self.sync_id)}/map.png', img_temp)

        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(ObjectsItem, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'


class SettingsPredefinedObjectsItems(models.Model):
    class Meta:
        verbose_name_plural = "Predefined Objects"

    setting = models.ForeignKey(Settings, models.CASCADE)
    predefined_object = models.OneToOneField(ObjectsItem, models.CASCADE)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(SettingsPredefinedObjectsItems, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'


class Collections(models.Model):
    class Meta:
        verbose_name_plural = "Collections"

    user = models.ForeignKey(Users, models.CASCADE, blank=True, null=True)
    objects_item = models.ManyToManyField(ObjectsItem)
    category = models.ManyToManyField(Categories)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True, max_length=110)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Collections, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'


class Categorieslocalizations(models.Model):
    class Meta:
        verbose_name_plural = "Categories Localizations"

    category = models.ForeignKey(Categories, models.CASCADE)
    title = models.CharField(max_length=45)
    language = models.CharField(max_length=45, choices=LOCALIZATIONS_CHOICES, default=LOCALIZATIONS_CHOICES.en)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Categorieslocalizations, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'


class ObjectsCategories(models.Model):
    class Meta:
        verbose_name_plural = "Objects Categories"

    objects_item = models.OneToOneField(ObjectsItem, models.CASCADE)
    category = models.ManyToManyField(Categories)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(ObjectsCategories, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'


class Chats(models.Model):
    class Meta:
        verbose_name_plural = "Chats"

    user = models.ForeignKey('Users', models.CASCADE)
    objects_item = models.OneToOneField('ObjectsItem', models.CASCADE)
    last_step = models.IntegerField()
    finished = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    history = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Chats, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'


class ObjectsImages(models.Model):
    class Meta:
        verbose_name_plural = "Objects Images"

    objects_item = models.ForeignKey(ObjectsItem, models.CASCADE)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True, max_length=110)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(ObjectsImages, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'


class ObjectsMap(models.Model):
    class Meta:
        verbose_name_plural = "Objects Map"

    objects_item = models.OneToOneField(ObjectsItem, related_name='object_map', on_delete=models.CASCADE)
    image = models.ImageField()
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def thumbnail(self):
        if getattr(self, 'image', None):
            return format_html('<img src="{}" width="280"/>'.format(self.image.url))
        else:
            return format_html("No map")

    thumbnail.allow_tags = True
    thumbnail.short_description = 'thumbnail'

    def __str__(self):
        return f'{self.id}'


class MuseumsImages(models.Model):
    class Meta:
        verbose_name_plural = "Museums Images"

    image = models.ImageField(upload_to=get_image_path, max_length=110)
    image_type = models.CharField(max_length=45, choices=IMAGE_TYPES, default=IMAGE_TYPES.smpl)
    museum = models.ForeignKey(Museums, models.CASCADE)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(MuseumsImages, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'


class ObjectsLocalizations(models.Model):
    class Meta:
        verbose_name_plural = "Objects Localizations"

    objects_item = models.ForeignKey(ObjectsItem, models.CASCADE)
    language = models.CharField(max_length=45, choices=LOCALIZATIONS_CHOICES, default=LOCALIZATIONS_CHOICES.en)
    conversation = models.FileField(upload_to=get_image_path, blank=True, null=True, max_length=110)
    description = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=45, blank=True, null=True)
    object_kind = models.CharField(max_length=45, blank=True, null=True)
    phrase = models.CharField(max_length=45, blank=True, null=True)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(ObjectsLocalizations, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'


class UsersLanguageStyles(models.Model):
    class Meta:
        verbose_name_plural = "Users Language Styles"

    user = models.OneToOneField(Users, models.CASCADE)
    language_style = models.CharField(max_length=45, choices=LANGUEAGE_STYLE_CHOICES, null=True, blank=True)
    score = models.IntegerField(blank=True, null=True)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(UsersLanguageStyles, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'


class Votings(models.Model):
    class Meta:
        verbose_name_plural = "Votings"

    user = models.ForeignKey(Users, models.CASCADE)
    objects_item = models.OneToOneField(ObjectsItem, models.CASCADE)
    vote = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Votings, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'