from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.gis.db import models
from django.contrib import messages
from django.forms.models import BaseInlineFormSet
from django.http import HttpResponseRedirect
from django.core.files.base import ContentFile
from main.variables import NUMBER_OF_LOCALIZATIONS
from main.models import MusemsTensor, TENSOR_STATUSES
from mapwidgets.widgets import GooglePointFieldWidget
from .models import Collections, Users, Settings, Museums, ObjectsItem,\
                    Categories, Categorieslocalizations, ObjectsCategories,\
                    ObjectsImages, Chats, ObjectsImages, MuseumsImages,\
                    ObjectsLocalizations, UsersLanguageStyles, Votings, \
                    PredefinedAvatars, SettingsPredefinedObjectsItems, \
                    ObjectsMap, MusemsTensor, SemanticRelationLocalization, \
                    SemanticRelation, OpenningTime, MuseumLocalization, \
                    MuseumTour, MuseumTourLocalization, TourObjectsItems, \
                    ObjectsTensorImage, UserTour
import json
import nested_admin
import boto3
import time
from timeloop import Timeloop
from datetime import timedelta
import logging
from botocore.exceptions import WaiterError
from collections import defaultdict

admin.site.site_header = "Museums Admin"
admin.site.site_title = "Museums Admin"

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


class MuseumTourLocalizationInline(MinValidatedInlineMixIn, nested_admin.NestedTabularInline):
    model = MuseumTourLocalization
    min_number = 1
    extra = 0
    readonly_fields = ['updated_at']


class TourObjectsItemsInline(MinValidatedInlineMixIn, nested_admin.NestedTabularInline):
    model = TourObjectsItems
    min_number = 1
    extra = 0
    readonly_fields = ['updated_at']


class MuseumTourInline(nested_admin.NestedTabularInline):
    inlines = [MuseumTourLocalizationInline, TourObjectsItemsInline] 
    model = MuseumTour
    extra = 0
    readonly_fields = ['updated_at']


class MuseumsImagesInline(nested_admin.NestedTabularInline):
    model = MuseumsImages
    extra = 0
    readonly_fields = ['updated_at']
    exclude = ('synced',)
    formset = MusImagesFormSet


class MusemsTensorInline(nested_admin.NestedTabularInline):
    model = MusemsTensor
    extra = 0
    exclude = ('synced', 'mobile_tensor_status', 'tensor_status')

    def has_change_permission(self, request, obj=None):
        return False


class MusemsOpeningInline(MinValidatedInlineMixIn, nested_admin.NestedTabularInline):
    model = OpenningTime
    min_number = 0
    extra = 1


class MuseumLocalizationInline(MinValidatedInlineMixIn, nested_admin.NestedTabularInline):
    readonly_fields = ['updated_at']
    model = MuseumLocalization
    extra = 0
    min_number = 1


class MuseumsAdmin(nested_admin.NestedModelAdmin):
    change_form_template = "admin/main/objectsitem/create_model.html"
    inlines = [MuseumLocalizationInline, MusemsOpeningInline,
               MuseumsImagesInline, MuseumTourInline, MusemsTensorInline]
    readonly_fields = ['updated_at', 'sync_id']
    exclude = ('synced',)
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }

    def _fetch_model(self, model_name, label_name, museum, mus_tensor, request):
        s3_resource = boto3.resource('s3')
        s3_client = boto3.client('s3')
        try:
            model_data = s3_client.get_object(Bucket='mein-objekt-tensorflow', Key=f'{museum.sync_id}/model/graph/{model_name}')
            label_data = s3_client.get_object(Bucket='mein-objekt-tensorflow', Key=f'{museum.sync_id}/model/label/{label_name}')
        except s3_client.exceptions.NoSuchKey:
            logging.error("Failed to generate a model")
            data = json.dumps({'musueum_id': str(museum.sync_id),'status': 'stopped'})
            s3_resource.Object('mein-objekt-tensorflow', 'instance_info.json').put(Body=data)
            mus_tensor.tensor_status = TENSOR_STATUSES['error']
            mus_tensor.mobile_tensor_status = TENSOR_STATUSES['error']
            mus_tensor.save()
            model_data, label_data = None, None
        return model_data, label_data, 

    def response_change(self, request, obj):
        if "_create_model" in request.POST:
            client = boto3.client('ec2')
            mobile_instance_id = 'i-008ee6f35a7616259'
            backend_instance_id = 'i-0a7688296bd1c764b'
            mus_pk = request.path.split('/')[-3]
            museum = Museums.objects.get(pk=mus_pk)
            mus_tensor = museum.museumtensor.first()
            if not mus_tensor:
                mus_tensor = MusemsTensor.objects.create(museum=museum)

            s3_resource = boto3.resource('s3')
            s3_client = boto3.client('s3')

            # check dataset and validate it
            try:
                response = s3_client.list_objects(Bucket='mein-objekt-tensorflow', Prefix=f'{museum.sync_id}/dataset')
            except:
                logging('Unsuccess images number validation')
            else:
                if not response.get('Contents', []):
                    messages.add_message(request, messages.INFO, 'No images found for museum TensorFlow model generation\
                                                                  Add at least 20 images for each object that you \
                                                                  want to be discoverable')
                    return HttpResponseRedirect(".")
                items_images = defaultdict(int)
                for i in response.get('Contents', []):
                    item = list(filter(lambda x: x != '', i['Key'].split('/')))
                    filtered_o_item = ObjectsItem.objects.filter(museum=museum).filter(sync_id=item[2])
                    if len(item) > 3 and filtered_o_item:
                        if item[3].split('.')[-1] not in ['jpg', 'jpeg', 'JPEG']:
                            messages.add_message(request, messages.INFO, 'All objects items images must be in jpeg format')
                            return HttpResponseRedirect(".")
                        items_images[item[2]] += 1
                less_then_20 = {i:k for i,k in items_images.items() if k < 20}
                if less_then_20:
                    messages.add_message(request, messages.INFO, f'At least 20 images must be uploaded for these \
                                                                   objects: {list(less_then_20.keys())}. Check if \
                                                                   some images may have same name or be added twice \
                                                                   (There must be 20 images with unique names)')
                    return HttpResponseRedirect(".")
            # check instance info if is not used by other museum
            instance_info = s3_client.get_object(Bucket='mein-objekt-tensorflow', Key='instance_info.json')
            instance_dict = json.loads(instance_info['Body'].read().decode('utf-8'))            
            if instance_dict['status'] == 'stopped':
                try:
                    # create dummy file because necessary directories for tensor instance
                    data = 'dummy_data'
                    s3_resource.Object('mein-objekt-tensorflow', f'{museum.sync_id}/model/graph/dummy.txt').put(Body=data)
                    s3_resource.Object('mein-objekt-tensorflow', f'{museum.sync_id}/model/label/dummy.txt').put(Body=data)
                    logging.info('S3 directories created')

                    # switch instance state to running
                    data = json.dumps({'musueum_id': str(museum.sync_id),'status': 'running'})
                    s3_resource.Object('mein-objekt-tensorflow', 'instance_info.json').put(Body=data)

                    # run instances
                    response = client.start_instances(  
                        InstanceIds=[
                            mobile_instance_id,
                            backend_instance_id
                        ],
                        DryRun=False
                    )
                except:
                    logging.error('Failed to start tensor instance')
                    messages.info(request, "Failed to start images processing, \
                                            please try later")
                else:
                    mus_tensor.tensor_status = TENSOR_STATUSES['processing']
                    mus_tensor.mobile_tensor_status = TENSOR_STATUSES['processing']
                    mus_tensor.save()
                    logging.info('Tensor flow processing started')
                    self.message_user(request, "Museum objects images are now processing into new Tensorflow model")

                    tl = Timeloop()
                    @tl.job(interval=timedelta(seconds=150))
                    def mobile_waiter_job():
                        try:
                            # check if model generate completed
                            waiter = client.get_waiter('instance_status_ok')
                            waiter.wait(InstanceIds=[mobile_instance_id],
                                        WaiterConfig={
                                            'Delay': 25,
                                            'MaxAttempts': 3
                                        })
                            logging.info("Mobile Instance working")
                        except:
                            logging.info('Mobile Instance stopped')
                            model_name = 'mobile_graph.pb'
                            label_name = 'mobile_label.txt'

                            # check if models created
                            model_data, label_data = self._fetch_model(model_name, label_name, museum, mus_tensor, request)
                            if not model_data and not label_data:
                                try:
                                    tl.stop()
                                except:
                                    return
                            # save models to django models
                            model_contents = model_data['Body'].read()
                            label_contents = label_data['Body'].read()
                            mobile_tensor = ContentFile(model_contents)
                            mobile_label = ContentFile(label_contents)

                            mus_tensor.mobile_tensor_status = TENSOR_STATUSES['ready']
                            mus_tensor.mobile_tensor_flow_model.save(model_name, mobile_tensor)
                            mus_tensor.mobile_tensor_flow_lables.save(label_name, mobile_label)
                            mus_tensor.save()

                            # stop workers if both models created 
                            if mus_tensor.tensor_status == TENSOR_STATUSES['ready']:
                                try:
                                    tl.stop()
                                except:
                                    data = json.dumps({'musueum_id': str(museum.sync_id),'status': 'stopped'})
                                    s3_resource.Object('mein-objekt-tensorflow', 'instance_info.json').put(Body=data)
                                    logging.info('Checking workers stopped')

                    @tl.job(interval=timedelta(seconds=150))
                    def backend_waiter_job():
                        try:
                            # check if model generate completed
                            waiter = client.get_waiter('instance_status_ok')
                            waiter.wait(InstanceIds=[backend_instance_id],
                                        WaiterConfig={
                                            'Delay': 25,
                                            'MaxAttempts': 35  
                                        })
                            logging.info("Backend Instance working")
                        except:
                            logging.info('Backend Instance stopped')
                            s3_client = boto3.client('s3')
                            model_name = 'backend_graph.pb'
                            label_name = 'backend_label.txt'
                            # check if models created
                            model_data, label_data = self._fetch_model(model_name, label_name, museum, mus_tensor, request)
                            if not model_data and not label_data:
                                try:
                                    tl.stop()
                                except:
                                    return
                            # save models to django models                            
                            model_contents = model_data['Body'].read()
                            label_contents = label_data['Body'].read()
                            backend_tensor = ContentFile(model_contents)
                            backend_label = ContentFile(label_contents)

                            mus_tensor.tensor_status = TENSOR_STATUSES['ready']
                            mus_tensor.tensor_flow_model.save(model_name, backend_tensor)
                            mus_tensor.tensor_flow_lables.save(label_name, backend_label)
                            mus_tensor.save()
                            if mus_tensor.mobile_tensor_status == TENSOR_STATUSES['ready']:
                                try:
                                    tl.stop()
                                except:
                                    data = json.dumps({'musueum_id': str(museum.sync_id),'status': 'stopped'})
                                    s3_resource.Object('mein-objekt-tensorflow', 'instance_info.json').put(Body=data)
                                    logging.info('Checking workers stopped')
                tl.start()
            else:
                messages.add_message(request, messages.INFO, 'Other museum images are being processing now \
                                                              please repeat in 20 minutes')
                return HttpResponseRedirect(".")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


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


class ObjectsTensorImageInline(admin.TabularInline):
    model = ObjectsTensorImage
    extra = 0
    fields = ('thumbnail','image')
    readonly_fields = ['thumbnail', 'updated_at', 'sync_id']
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
               ObjectsCategoriesInline, ObjectsMapInline, 
               ObjectsTensorImageInline]
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
    readonly_fields = ['objects_item', 'last_step', 'history', 'finished', 'planned', 'updated_at', 'sync_id']
    fields = ('objects_item', 'last_step', 'history', 'finished', 'planned', 'updated_at', 'sync_id')
    exclude = ('synced',)

class UserTourInline(admin.TabularInline):
    model = UserTour
    extra = 0
    readonly_fields = ['museum_tour', 'updated_at', 'sync_id']
    fields = ('museum_tour', 'updated_at', 'sync_id', )
    exclude = ('synced',)

class UsersAdmin(admin.ModelAdmin):
    inlines = [UsersLanguageStylesInline, VotingsInline, CollectionsInline,
               ChatsInline, UserTourInline]
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
