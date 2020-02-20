from django.contrib.postgres.fields import JSONField, ArrayField
from django.contrib.gis.db import models
from django.contrib import messages
from django.utils import timezone
from django.utils.html import format_html
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import transaction
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
from django.conf import settings
from main.variables import DEFAULT_MUSEUM, MIN_TENSOR_IMAGE_SIZE
from model_utils import Choices

import cchardet
import urllib
import uuid
import os
from multiselectfield import MultiSelectField
from storages.backends.s3boto3 import S3Boto3Storage
import boto3
import logging


storing = boto3.setup_default_session(region_name='eu-central-1')

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
        ('logo', 'Logo'),
        ('pnt', 'Pointer'),
        ('1_map', 'First floor map'),
        ('2_map', 'Second floor map'),
        ('3_map', 'Third floor map'),
      )

WEEKDAYS = Choices(
    ('monday', ("Monday")),
    ('tuesday', ("Tuesday")),
    ('wednesday', ("Wednesday")),
    ('thursday', ("Thursday")),
    ('friday', ("Friday")),
    ('suturday', ("Saturday")),
    ('sunday', ("Sunday")),
 )

TENSOR_STATUSES = Choices(
        ('none', 'None'),
        ('ready', 'Ready!'),
        ('processing', 'processing...'),
        ('validating', 'validating...'),
        ('error', 'Model creation error, please add more objects with tensor images')
      )

LEVELS_CHOICES = [
        ('0', 0),
        ('1', 1),
        ('2', 2),
        ('3', 3),
      ]


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
                museum_name = str(getattr(item, 'museum', None).sync_id)
                object_syncid = getattr(item, 'sync_id', None)
        dir_name = f'Museum/{museum_name}'
        if instance.__class__.__name__ == 'MuseumsImages':
            museum_name = instance.museum
        if instance.__class__.__name__ in ('ObjectsItem', 'ObjectsImages', 'ObjectsLocalizations'):
            dir_name += f'/Objects/{object_syncid}'
        if instance.__class__.__name__ == 'PredefinedAvatars':
            dir_name = f'Museum/PredefinedAvatars'
    return os.path.join('images', dir_name, filename)

def  get_tensor_image_path(instance, filename):
    ob_item = instance.objects_item
    museum = ob_item.museum
    data_dir = 'dataset'
    if ObjectsTensorImage.objects.filter(objects_item=ob_item).count() <= 20:
        data_dir ='temp_dataset'
    return os.path.join(str(museum.sync_id), data_dir, str(ob_item.sync_id), filename)


def validate_percent(value):
    if value < 0 or value > 100:
        raise ValidationError('Value must be between 0-100',
                              params={'value': value})


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

@receiver(pre_delete, sender=Categories, dispatch_uid="create_delete_category")
def create_delete_category(sender, instance, **kwargs):
    DeletedItems.objects.create(category=instance.sync_id)


class Users(models.Model):
    class Meta:
        verbose_name_plural = "Users"

    name = models.CharField(max_length=45, blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True)
    device_id = models.CharField(max_length=45, blank=True, null=True, default=None)
    category = models.ForeignKey(Categories, models.CASCADE, blank=True, null=True)
    positionx = models.DecimalField(db_column='positionX', max_digits=4, decimal_places=0, default=0)
    positiony = models.DecimalField(db_column='positionY', max_digits=4, decimal_places=0, default=0)
    floor = models.IntegerField(blank=True, null=True, default=0)
    language = models.CharField(max_length=45, choices=LOCALIZATIONS_CHOICES, default=LOCALIZATIONS_CHOICES.en)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    user_level = models.CharField(max_length=45, choices=LEVELS_CHOICES,
                                default=0)
    font_size = models.CharField(max_length=45, blank=True, null=True, default=None)
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


class Settings(models.Model):
    class Meta:
        verbose_name_plural = "Settings"

    position_score = JSONField(default=list)
    site_url = models.URLField(blank=True, null=True)
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
    language_styles = MultiSelectField(choices=LANGUEAGE_STYLE_CHOICES,
                                 max_choices=4,
                                 max_length=80)
    save_collections_to_tensor = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid4,editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    # collections = models.ForeignKey(Collection, models.DO_NOTHING)
    recognition_threshold = models.SmallIntegerField(default=50,
                                                     validators=[validate_percent])

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

    floor_amount = models.IntegerField()
    ratio_pixel_meter = models.FloatField(blank=True, null=True)
    museum_site_url = models.URLField(blank=True, null=True)
    settings = models.ForeignKey(Settings, models.SET_NULL, null=True)
    location = models.PointField(null=True)
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
            return self.objectsitem_set.filter(sync_id__in=self._objects_to_serialize)
        else:
            return self.objectsitem_set.all()

    @property
    def objectsitems(self):
        return self.objectsitem_set.all()

    @property
    def museumimages(self):
        return self.museumsimages_set.all()

    @property
    def opennings(self):
        return self.openningtime_set.first()

    @property
    def localizatoins(self):
        return self.localizations_set.all()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Museums, self).save(*args, **kwargs)

    def __str__(self):
        if self.localizations.filter(language="en").exists():
            return f'{self.localizations.get(language="en").title}'
        elif self.localizations.filter(language="de").exists():
            return f'{self.localizations.get(language="de").title}'
        else:
            return f'{self.id}'


class MuseumLocalization(models.Model):
    museum = models.ForeignKey(Museums, on_delete=models.CASCADE,
                               related_name='localizations',
                               related_query_name='localizations')
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    language = models.CharField(max_length=45, choices=LOCALIZATIONS_CHOICES,
                                default=LOCALIZATIONS_CHOICES.en)
    title = models.CharField(max_length=45, default=DEFAULT_MUSEUM)
    specialization = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.language}'

    def clean(self):
        super().clean()

        id = self.id
        title = self.title
        language = self.language
        museum = self.museum

        validate_title = MuseumLocalization.objects.filter(title=title)\
            .exclude(museum=museum).exists()
        validate_language = MuseumLocalization.objects\
            .filter(language=language, museum=museum)\
            .exclude(id=id)\
            .exists()

        if validate_language:
            raise ValidationError('Language is already exists')

        if validate_title:
            raise ValidationError('Title is already exists')


class OpenningTime(models.Model):
    museum = models.ForeignKey(Museums, models.SET_NULL, null=True)
    weekday = MultiSelectField(choices=WEEKDAYS, max_length=110)
    from_hour = models.TimeField()
    to_hour = models.TimeField()


class MusemsTensor(models.Model):
    class Meta:
        verbose_name_plural = "Tensor flow models"

    museum = models.ForeignKey(Museums, models.PROTECT, related_name='museumtensor')
    tensor_flow_model = models.FileField(upload_to='tensor_model/', blank=True, null=True, max_length=110)
    tensor_flow_lables = models.FileField(upload_to='tensor_label/', blank=True, null=True, max_length=110)
    mobile_tensor_flow_model = models.FileField(upload_to='tensor_model/', blank=True, null=True, max_length=110)
    mobile_tensor_flow_lables = models.FileField(upload_to='tensor_label/', blank=True, null=True, max_length=110)
    tensor_status = models.CharField(max_length=145, choices=TENSOR_STATUSES, default='none')
    mobile_tensor_status = models.CharField(max_length=145, choices=TENSOR_STATUSES, default='none')
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(MusemsTensor, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'


class ObjectsItem(models.Model): 
    class Meta:
        verbose_name_plural = "Objects"

    priority = models.IntegerField(choices=PRIORITY_CHOICES,
        default=PRIORITY_CHOICES.first)
    museum = models.ForeignKey(Museums, models.PROTECT)
    floor = models.IntegerField()
    positionx = models.DecimalField(db_column='positionX', max_digits=4, decimal_places=0)
    positiony = models.DecimalField(db_column='positionY', max_digits=4, decimal_places=0)
    vip = models.BooleanField(default=False)
    author = models.CharField(max_length=145, blank=True, null=True)
    language_style = models.CharField(max_length=45, choices=LANGUEAGE_STYLE_CHOICES, default='easy')
    avatar = models.ImageField(upload_to=get_image_path, blank=True, null=True, max_length=110)
    cropped_avatar = models.ImageField(upload_to=get_image_path, blank=True, null=True, max_length=110)
    onboarding = models.BooleanField(default=False)
    semantic_relation = models.ManyToManyField('self', through='SemanticRelation', symmetrical=False)
    in_tensor_model = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    synced = models.BooleanField(default=False)
    object_level = models.CharField(max_length=45, choices=LEVELS_CHOICES,
                                default=0)
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
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(ObjectsItem, self).save(*args, **kwargs)

    def __str__(self):
        if self.localizations.filter(language="en").exists():
            return f'{self.localizations.get(language="en").title}'
        elif self.localizations.filter(language="de").exists():
            return f'{self.localizations.get(language="de").title}'
        else:
            return f'{self.id}'


class MuseumTour(models.Model):
    museum = models.ForeignKey(Museums, models.CASCADE,
                               related_name='tours',
                               related_query_name='tours')
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(MuseumTour, self).save(*args, **kwargs)


class MuseumTourLocalization(models.Model):
    tour = models.ForeignKey(MuseumTour, on_delete=models.CASCADE,
                               related_name='localizations',
                               related_query_name='localizations')
    language = models.CharField(max_length=45, choices=LOCALIZATIONS_CHOICES,
                                default=LOCALIZATIONS_CHOICES.en)
    title = models.CharField(max_length=45, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(MuseumTourLocalization, self).save(*args, **kwargs)


class TourObjectsItems(models.Model):
    tour = models.ForeignKey(MuseumTour, on_delete=models.CASCADE,
                               related_name='tourobjects',
                               related_query_name='tourobjects')
    tour_object = models.ForeignKey(ObjectsItem, models.CASCADE, default=1,
                               related_name='tourobjects',
                               related_query_name='tourobjects')
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(TourObjectsItems, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'


class UserTour(models.Model):
    user = models.ForeignKey(Users, models.CASCADE, blank=True, null=True,
                               related_name='user_tours',
                               related_query_name='user_tours')
    museum_tour = models.ForeignKey(MuseumTour, models.CASCADE,
                               related_name='user_tour',
                               related_query_name='user_tour')
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(UserTour, self).save(*args, **kwargs)


class SemanticRelation(models.Model):
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    from_object_item = models.ForeignKey(ObjectsItem,
                                         on_delete=models.CASCADE,
                                         related_name='from_object_item')
    to_object_item = models.ForeignKey(ObjectsItem,
                                       on_delete=models.CASCADE,
                                       related_name='to_object_item')
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.updated_at = timezone.now()
        self.from_object_item.updated_at = timezone.now()
        self.from_object_item.save()
        self.to_object_item.updated_at = timezone.now()
        self.to_object_item.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.from_object_item} - {self.to_object_item}'


class SemanticRelationLocalization(models.Model):
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False)
    objects_item = models.ForeignKey(SemanticRelation, models.CASCADE,
                                     related_name='localizations',
                                     related_query_name='localizations')
    language = models.CharField(max_length=45, choices=LOCALIZATIONS_CHOICES,
                                default=LOCALIZATIONS_CHOICES.en)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.language}'


@receiver(pre_delete, sender=ObjectsItem, dispatch_uid="create_delete_object")
def create_delete_objects(sender, instance, **kwargs):
    DeletedItems.objects.create(objects_item=instance.sync_id)


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
    objects_item = models.ForeignKey(ObjectsItem, models.CASCADE)
    category = models.ManyToManyField(Categories)
    image = models.ImageField(max_length=110)
    sync_id = models.UUIDField(default=uuid.uuid4, unique=True)
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

@receiver(post_save, sender=Collections, dispatch_uid="create_objecttensor")
def create_objecttensor(sender, instance, **kwargs):
    museum = Museums.objects.get(objectsitem=instance.objects_item)
    col_image = instance.image
    name = col_image.name.split("/")[-1]
    ext = name.split('.')[-1]
    if getattr(museum.settings, 'save_collections_to_tensor', None) and \
                         col_image.size > MIN_TENSOR_IMAGE_SIZE and \
                         ext in ['jpg', 'jpeg', 'JPG', 'JPEG']:
        image_copy = ContentFile(col_image.read())
        tensorimage_instance = ObjectsTensorImage()
        tensorimage_instance.objects_item = instance.objects_item
        tensorimage_instance.image.save(name, image_copy)
        tensorimage_instance.save()

class Categorieslocalizations(models.Model):
    class Meta:
        verbose_name_plural = "Categories Localizations"

    category = models.ForeignKey(Categories, models.CASCADE)
    title = models.CharField(max_length=45)
    language = models.CharField(max_length=45, choices=LOCALIZATIONS_CHOICES, default=LOCALIZATIONS_CHOICES.en)
    description = models.TextField(blank=True, null=True)
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
            transaction.on_commit(self.update_role)
        self.updated_at = timezone.now()
        return super(ObjectsCategories, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'

    def update_role(self):        
        [i.save() for i in self.category.all()]


class Chats(models.Model):
    class Meta:
        verbose_name_plural = "Chats"

    user = models.ForeignKey('Users', models.CASCADE)
    objects_item = models.ForeignKey('ObjectsItem', models.CASCADE)
    last_step = models.IntegerField()
    finished = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid4, unique=True)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    history = models.TextField(blank=True, null=True)
    planned = models.BooleanField(default=False)

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

    number = models.PositiveSmallIntegerField()
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


class ObjectsTensorImage(models.Model):
    class Meta:
        verbose_name_plural = "Objects Tensor Images"

    objects_item = models.ForeignKey(ObjectsItem, related_name='object_tensor_image', on_delete=models.CASCADE)
    image = models.ImageField(storage=S3Boto3Storage(bucket='mein-objekt-tensorflow'),
                              upload_to=get_tensor_image_path, max_length=110,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'JPG', 'JPEG'])])
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
            return format_html('<img src="{}" width="80"/>'.format(self.image.url))
        else:
            return format_html("No image")

    thumbnail.allow_tags = True
    thumbnail.short_description = 'thumbnail'

    def __str__(self):
        return f'{self.id}'

@receiver(post_save, sender=ObjectsTensorImage, dispatch_uid="check_20")
def check_20(sender, instance, **kwargs):
    ob_item = instance.objects_item
    museum = ob_item.museum
    bucket = 'mein-objekt-tensorflow'

    if ObjectsTensorImage.objects.filter(objects_item=ob_item).count() == 20:
        s3_client = boto3.client('s3')
        try:
            response = s3_client.list_objects(Bucket=bucket, Prefix=f'{museum.sync_id}/temp_dataset')
        except:
            logging('Unsuccess images number validation')
        else:
            for i in response.get('Contents', []):
                item = list(filter(lambda x: x != '', i['Key'].split('/')))
                source_key = os.path.join(*item)
                item[1] = 'dataset'
                dest_key = os.path.join(*item)
                copy_source = {'Bucket': bucket, 'Key': source_key}
                s3_client.copy_object(CopySource=copy_source, Bucket=bucket, Key=dest_key)
                # TODO make just django image model path change to new destination before deletion
                # s3_client.delete_object(Bucket=bucket, Key=source_key) 


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
    conversation = models.FileField(upload_to=get_image_path, blank=True, null=True, max_length=110,
                                    validators=[FileExtensionValidator(allowed_extensions=['txt'])])
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

    def clean(self):
        if self.conversation:            
            chat = self.conversation.read()
            try:
                encoding = cchardet.detect(chat)['encoding']
                if encoding.upper() != 'UTF-8':
                    raise ValidationError('Bad convarsation file encoding. It should be UTF-8')

                    #TODO discover converting encodings withour losses
                    # newchat = chat.decode(encoding).encode('utf-8')
                    # self.conversation.save(f'utf-8_{self.conversation.name}', ContentFile(newchat))
            except:
                raise ValidationError('Bad convarsation file encoding. It should be UTF-8')

    def __str__(self):
        return f'{self.id}'


class UsersLanguageStyles(models.Model):
    class Meta:
        verbose_name_plural = "Users Language Styles"

    user = models.OneToOneField(Users, models.CASCADE)
    language_style = JSONField(max_length=145, blank=True, null=True, default=list)
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
    objects_item = models.ForeignKey(ObjectsItem, models.CASCADE)
    vote = models.BooleanField(default=False)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
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


class DeletedItems(models.Model):
    class Meta:
        verbose_name_plural = "Deleted Items"

    objects_item = models.UUIDField(blank=True, null=True)
    category = models.UUIDField(blank=True, null=True)
    sync_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(DeletedItems, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'