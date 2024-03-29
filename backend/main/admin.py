from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.files.temp import NamedTemporaryFile
from django import forms
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.gis.db import models
from django.contrib import messages
from django.conf import settings
from django.forms.models import BaseInlineFormSet
from django.forms import widgets
from django.http import HttpResponseRedirect
from django.core.files.base import ContentFile
from main.variables import (
    NUMBER_OF_LOCALIZATIONS,
    MIN_TENSOR_IMAGE_SIZE,
    MAX_TENSOR_IMAGE_SIZE,
)
from main.models import MusemsTensor, TENSOR_STATUSES
from main.apps import tensors
from mapwidgets.widgets import GooglePointFieldWidget
from .models import (
    Collections,
    Users,
    Settings,
    Museums,
    ObjectsItem,
    Categories,
    Categorieslocalizations,
    ObjectsCategories,
    ObjectsImages,
    Chats,
    ObjectsImages,
    MuseumsImages,
    ObjectsLocalizations,
    UsersLanguageStyles,
    Votings,
    PredefinedAvatars,
    SettingsPredefinedObjectsItems,
    ObjectsMap,
    MusemsTensor,
    SemanticRelationLocalization,
    SemanticRelation,
    OpenningTime,
    MuseumLocalization,
    MuseumTour,
    MuseumTourLocalization,
    TourObjectsItems,
    ObjectsTensorImage,
    UserTour,
    SuggestedObject,
    ChatDesigner,
    SingleLine,
    SingleLineLocalization,
    LANGUEAGE_STYLE_CHOICES,
    CHAT_MULTI_CHOICES,
)
import json
import nested_admin
import boto3
import time
from timeloop import Timeloop
from datetime import timedelta
import logging
from botocore.exceptions import WaiterError
from collections import defaultdict
from PIL import Image
from io import BytesIO

admin.site.site_header = "MeinObjekt"
admin.site.site_title = "MeinObjekt"

logger = logging.getLogger("django")
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter,
    RelatedDropdownFilter,
    ChoiceDropdownFilter,
)


class MinValidatedInlineMixIn:
    validate_min = True

    def get_formset(self, *args, **kwargs):
        return super().get_formset(validate_min=self.validate_min, *args, **kwargs)


class PredefinedAvatarsInline(MinValidatedInlineMixIn, admin.TabularInline):
    model = PredefinedAvatars
    min_num = 0  # should be 6
    extra = 0
    readonly_fields = ["updated_at"]
    exclude = ("synced",)


class SettingsPredefinedObjectsItemsInline(
    MinValidatedInlineMixIn, admin.TabularInline
):
    model = SettingsPredefinedObjectsItems
    min_num = 0
    extra = 0
    readonly_fields = ["updated_at"]
    exclude = ("synced",)


class SettingsAdmin(admin.ModelAdmin):
    inlines = [PredefinedAvatarsInline, SettingsPredefinedObjectsItemsInline]
    readonly_fields = ["updated_at"]
    exclude = ("synced",)


class MusImagesFormSet(BaseInlineFormSet):
    def clean(self):
        super(MusImagesFormSet, self).clean()

        mus_image_types = [i.instance.image_type for i in self.forms]
        map_types = [True for i in mus_image_types if "map" in i]
        pointer_types = [True for i in mus_image_types if "pnt" in i]
        logo_types = [True for i in mus_image_types if "logo" in i]

        if not any(map_types):
            raise ValidationError(
                'There must be at least one map image with type "<number> floor map"!'
            )
        if len(pointer_types) != 1:
            raise ValidationError(
                'There must be exatly one pointer image with type "Pointer"!'
            )
        if len(logo_types) != 1:
            raise ValidationError('There must be one image with type "Logo"!')


class MuseumTourLocalizationInline(
    MinValidatedInlineMixIn, nested_admin.NestedTabularInline
):
    model = MuseumTourLocalization
    min_number = 1
    extra = 0
    readonly_fields = ["updated_at"]


class TourObjectsItemsInline(MinValidatedInlineMixIn, nested_admin.NestedTabularInline):
    model = TourObjectsItems
    min_number = 1
    extra = 0
    readonly_fields = ["updated_at"]


class MuseumTourInline(nested_admin.NestedTabularInline):
    inlines = [MuseumTourLocalizationInline, TourObjectsItemsInline]
    model = MuseumTour
    extra = 0
    readonly_fields = ["updated_at"]


class MuseumsImagesInline(nested_admin.NestedTabularInline):
    model = MuseumsImages
    extra = 0
    readonly_fields = ["updated_at"]
    exclude = ("synced",)
    formset = MusImagesFormSet


class MusemsTensorInline(nested_admin.NestedTabularInline):
    model = MusemsTensor
    extra = 0
    exclude = ("synced", "mobile_tensor_status", "tensor_status")

    def has_change_permission(self, request, obj=None):
        return False


class MusemsOpeningInline(MinValidatedInlineMixIn, nested_admin.NestedTabularInline):
    model = OpenningTime
    min_number = 0
    extra = 0


class MuseumLocalizationInline(
    MinValidatedInlineMixIn, nested_admin.NestedTabularInline
):
    readonly_fields = ["updated_at"]
    model = MuseumLocalization
    extra = 0
    min_number = 1


class MuseumsAdmin(nested_admin.NestedModelAdmin):
    list_display = ["id", "localizations", "objects_number", "sync_id"]
    change_form_template = "admin/main/museum/create_model.html"
    inlines = [
        MuseumLocalizationInline,
        MusemsOpeningInline,
        MuseumsImagesInline,
        MuseumTourInline,
        MusemsTensorInline,
    ]
    readonly_fields = ["updated_at", "sync_id"]
    exclude = ("synced",)
    formfield_overrides = {models.PointField: {"widget": GooglePointFieldWidget}}

    def localizations(self, obj):
        return getattr(obj.localizations.first(), "title", "No title")

    def objects_number(self, obj):
        return obj.objectsitem_set.count()

    def _fetch_model(self, model_name, label_name, museum, mus_tensor, request):
        s3_resource = boto3.resource("s3")
        s3_client = boto3.client("s3")
        try:
            model_data = s3_client.get_object(
                Bucket="mein-objekt-tensorflow",
                Key=f"{museum.sync_id}/model/graph/{model_name}",
            )
            label_data = s3_client.get_object(
                Bucket="mein-objekt-tensorflow",
                Key=f"{museum.sync_id}/model/label/{label_name}",
            )
        except s3_client.exceptions.NoSuchKey:
            logger.error("Failed to fetch a model or label")
            data = json.dumps({"musueum_id": str(museum.sync_id), "status": "stopped"})
            s3_resource.Object("mein-objekt-tensorflow", "instance_info.json").put(
                Body=data
            )
            mus_tensor.tensor_status = TENSOR_STATUSES["error"]
            mus_tensor.mobile_tensor_status = TENSOR_STATUSES["error"]
            mus_tensor.save()
            model_data, label_data = None, None
        return (
            model_data,
            label_data,
        )

    def response_change(self, request, obj):
        if "_create_model" in request.POST:
            ec2_client = boto3.client(
                "ec2",
                aws_access_key_id=settings.WEB_APP_USER_KEY,
                aws_secret_access_key=settings.WEB_APP_USER_SECRET,
            )
            mobile_instance_id = "i-008ee6f35a7616259"
            backend_instance_id = "i-0a7688296bd1c764b"
            mus_pk = request.path.split("/")[-3]
            museum = Museums.objects.get(pk=mus_pk)
            mus_tensor = museum.museumtensor.first()
            if not mus_tensor:
                mus_tensor = MusemsTensor.objects.create(museum=museum)

            s3_resource = boto3.resource("s3")
            s3_client = boto3.client("s3")

            # check dataset and validate it
            try:
                response = s3_client.list_objects(
                    Bucket="mein-objekt-tensorflow", Prefix=f"{museum.sync_id}/dataset"
                )
            except:
                logger("Unsuccess images number validation")
            else:
                if not response.get("Contents", []):
                    messages.add_message(
                        request,
                        messages.WARNING,
                        "No images found for museum TensorFlow model generation\
                                                                  Add at least 20 images for each object that you \
                                                                  want to be discoverable",
                    )
                    return HttpResponseRedirect(".")
                items_images = defaultdict(int)
                for i in response.get("Contents", []):
                    item = list(filter(lambda x: x != "", i["Key"].split("/")))
                    filtered_o_item = ObjectsItem.objects.filter(museum=museum).filter(
                        sync_id=item[2]
                    )
                    if len(item) > 3 and filtered_o_item:
                        if item[3].split(".")[-1] not in ["jpg", "jpeg", "JPEG", "JPG"]:
                            messages.add_message(
                                request,
                                messages.WARNING,
                                "All objects items images must be in jpeg format",
                            )
                            return HttpResponseRedirect(".")
                        items_images[item[2]] += 1
                less_then_20 = {i: k for i, k in items_images.items() if k < 20}
                if less_then_20:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        f"At least 20 images must be uploaded for these \
                                                                   objects: {list(less_then_20.keys())}. Check if \
                                                                   some images may have same name or be added twice \
                                                                   (There must be 20 images with unique names)",
                    )
                    return HttpResponseRedirect(".")
            # check instance info if is not used by other museum
            instance_info = s3_client.get_object(
                Bucket="mein-objekt-tensorflow", Key="instance_info.json"
            )
            instance_dict = json.loads(instance_info["Body"].read().decode("utf-8"))
            if instance_dict["status"] == "stopped":
                try:
                    # create dummy file because necessary directories for tensor instance
                    data = "dummy_data"
                    s3_resource.Object(
                        "mein-objekt-tensorflow",
                        f"{museum.sync_id}/model/graph/dummy.txt",
                    ).put(Body=data)
                    s3_resource.Object(
                        "mein-objekt-tensorflow",
                        f"{museum.sync_id}/model/label/dummy.txt",
                    ).put(Body=data)
                    logger.info("S3 directories created")
                    # switch instance state to running
                    data = json.dumps(
                        {"musueum_id": str(museum.sync_id), "status": "running"}
                    )
                    s3_resource.Object(
                        "mein-objekt-tensorflow", "instance_info.json"
                    ).put(Body=data)

                    # run instances
                    response = ec2_client.start_instances(
                        InstanceIds=[mobile_instance_id, backend_instance_id],
                        DryRun=False,
                    )
                except Exception as e:
                    # switch instance state to running
                    data = json.dumps(
                        {"musueum_id": str(museum.sync_id), "status": "stopped"}
                    )
                    s3_resource.Object(
                        "mein-objekt-tensorflow", "instance_info.json"
                    ).put(Body=data)
                    logger.error(f"Failed to start tensor instance: {e}")
                    messages.info(
                        request,
                        "Failed to start images processing, \
                                            please try later",
                    )
                    return HttpResponseRedirect(".")
                else:
                    mus_tensor.tensor_status = TENSOR_STATUSES["processing"]
                    mus_tensor.mobile_tensor_status = TENSOR_STATUSES["processing"]
                    mus_tensor.save()
                    logger.info("Tensor flow processing started")
                    self.message_user(
                        request,
                        "Museum objects images are now processing into new Tensorflow model",
                    )

                    tl = Timeloop()

                    @tl.job(interval=timedelta(seconds=150))
                    def mobile_waiter_job():
                        try:
                            # check if model generate completed
                            waiter = ec2_client.get_waiter("instance_status_ok")
                            waiter.wait(
                                InstanceIds=[mobile_instance_id],
                                WaiterConfig={"Delay": 25, "MaxAttempts": 3},
                            )
                            logger.info("Mobile Instance working")
                        except:
                            logger.info("Mobile Instance stopped")
                            model_name = "mobile_graph.pb"
                            label_name = "mobile_label.txt"

                            # check if models created
                            model_data, label_data = self._fetch_model(
                                model_name, label_name, museum, mus_tensor, request
                            )
                            if not model_data or not label_data:
                                try:
                                    tl.stop()
                                except:
                                    return
                            # save models to django models
                            model_contents = model_data["Body"].read()
                            label_contents = label_data["Body"].read()
                            mobile_tensor = ContentFile(model_contents)
                            mobile_label = ContentFile(label_contents)

                            mus_tensor.mobile_tensor_status = TENSOR_STATUSES["ready"]
                            mus_tensor.mobile_tensor_flow_model.save(
                                f"{museum.sync_id}/model/graph/{model_name}",
                                mobile_tensor,
                            )
                            mus_tensor.mobile_tensor_flow_lables.save(
                                f"{museum.sync_id}/model/label/{label_name}",
                                mobile_label,
                            )
                            mus_tensor.save()

                            # stop workers if both models created
                            if mus_tensor.tensor_status == TENSOR_STATUSES["ready"]:
                                try:
                                    tl.stop()
                                except:
                                    data = json.dumps(
                                        {
                                            "musueum_id": str(museum.sync_id),
                                            "status": "stopped",
                                        }
                                    )
                                    s3_resource.Object(
                                        "mein-objekt-tensorflow", "instance_info.json"
                                    ).put(Body=data)
                                    logger.info("Checking workers stopped")

                    @tl.job(interval=timedelta(seconds=150))
                    def backend_waiter_job():
                        try:
                            # check if model generate completed
                            waiter = ec2_client.get_waiter("instance_status_ok")
                            waiter.wait(
                                InstanceIds=[backend_instance_id],
                                WaiterConfig={"Delay": 25, "MaxAttempts": 3},
                            )
                            logger.info("Backend Instance working")
                        except:
                            logger.info("Backend Instance stopped")
                            model_name = "backend_graph.pb"
                            label_name = "backend_label.txt"
                            # check if models created
                            model_data, label_data = self._fetch_model(
                                model_name, label_name, museum, mus_tensor, request
                            )
                            if not model_data or not label_data:
                                try:
                                    tl.stop()
                                except:
                                    return
                            # save models to django models
                            model_contents = model_data["Body"].read()
                            label_contents = label_data["Body"].read()
                            backend_tensor = ContentFile(model_contents)
                            backend_label = ContentFile(label_contents)

                            mus_tensor.tensor_status = TENSOR_STATUSES["ready"]
                            mus_tensor.tensor_flow_model.save(
                                f"{museum.sync_id}/model/graph/{model_name}",
                                backend_tensor,
                            )
                            mus_tensor.tensor_flow_lables.save(
                                f"{museum.sync_id}/model/label/{label_name}",
                                backend_label,
                            )
                            mus_tensor.save()
                            tensors[museum.sync_id] = {
                                "tensor_flow_model": model_contents,
                                "tensor_flow_lables": label_contents,
                            }
                            if (
                                mus_tensor.mobile_tensor_status
                                == TENSOR_STATUSES["ready"]
                            ):
                                try:
                                    tl.stop()
                                except:
                                    data = json.dumps(
                                        {
                                            "musueum_id": str(museum.sync_id),
                                            "status": "stopped",
                                        }
                                    )
                                    s3_resource.Object(
                                        "mein-objekt-tensorflow", "instance_info.json"
                                    ).put(Body=data)
                                    labels = str(label_contents, "utf8").split("\n")
                                    labels = list(filter(None, labels))
                                    for label in labels:
                                        sync_id = "-".join(label.split(" "))
                                        ObjectsItem.objects.filter(
                                            sync_id=sync_id
                                        ).update(in_tensor_model=True)
                                    logger.info("Checking workers stopped")

                    tl.start()
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Other museum images are being processing now \
                                                              please repeat in 20 minutes",
                )
                return HttpResponseRedirect(".")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


class ObjectsImagesInline(nested_admin.NestedTabularInline):
    model = ObjectsImages
    extra = 0
    readonly_fields = ["updated_at"]
    exclude = ("synced",)


class ObjectsLocalizationsInline(
    MinValidatedInlineMixIn, nested_admin.NestedTabularInline
):
    model = ObjectsLocalizations
    min_num = NUMBER_OF_LOCALIZATIONS
    extra = 0
    readonly_fields = ["updated_at"]
    exclude = ("synced",)
    formfield_overrides = {
        models.TextField: {
            "widget": widgets.Textarea(
                attrs={"rows": 1, "cols": 40, "style": "height: 6em;"}
            )
        },
        models.CharField: {
            "widget": widgets.TextInput(
                attrs={"rows": 1, "cols": 40, "style": "height: 6em;"}
            )
        },
    }


class ObjectsCategoriesInline(
    MinValidatedInlineMixIn, nested_admin.NestedTabularInline
):
    model = ObjectsCategories
    min_num = 1
    extra = 0
    readonly_fields = ["updated_at"]
    exclude = ("synced",)


class ObjectsMapInlineFormset(forms.models.BaseInlineFormSet):
    def save_new(self, form, commit=True):
        # Ensure the latest copy of the related instance is present on each
        # form (it may have been saved after the formset was originally
        # instantiated).
        setattr(form.instance, self.fk.name, self.instance)
        # Use commit=False so we can assign the parent key afterwards, then
        # save the object.
        obj = form.save(commit=False)
        pk_value = getattr(self.instance, self.fk.remote_field.field_name)
        setattr(obj, self.fk.get_attname(), getattr(pk_value, "pk", pk_value))
        if commit:
            obj.save()
        if commit and hasattr(form, "save_m2m"):
            form.save_m2m()
        return obj


class ObjectsMapInline(nested_admin.NestedTabularInline):
    model = ObjectsMap
    extra = 0
    fields = ("thumbnail",)
    readonly_fields = ["thumbnail"]
    exclude = ("synced",)
    formset = ObjectsMapInlineFormset
    verbose_name_plural = "Object map, autogenerated after each object save (if position does not \
                                change after saving an object, please reload page with Ctrl+R)"

    def has_add_permission(self, request):
        return False


class ObjectsTensorImageInline(nested_admin.NestedTabularInline):
    model = ObjectsTensorImage
    extra = 0
    fields = ("thumbnail", "image")
    readonly_fields = ["thumbnail", "updated_at", "sync_id"]
    exclude = ("synced",)
    classes = ["collapse"]
    verbose_name_plural = "Saved Tensor Images (for better performance do not upload more than 10 \
                                    images at a time)"

    def has_add_permission(self, request, obj=None):
        return False


class SemanticRelatedLocalizationInline(nested_admin.NestedTabularInline):
    readonly_fields = [
        "updated_at",
    ]
    model = SemanticRelationLocalization
    extra = 0


class SemanticRelationForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        to_object_item = cleaned_data.get("to_object_item")
        from_object_item = self.cleaned_data.get("from_object_item")

        if to_object_item and from_object_item:

            if to_object_item == from_object_item:
                raise forms.ValidationError(
                    "Semantic relation to self can not be created"
                )

            if not self.instance.id:
                relations1 = SemanticRelation.objects.filter(
                    to_object_item=to_object_item, from_object_item=from_object_item
                ).exists()
                relations2 = SemanticRelation.objects.filter(
                    to_object_item=from_object_item, from_object_item=to_object_item
                ).exists()

                if relations1 or relations2:
                    raise forms.ValidationError("This semantic relation already exists")

        return cleaned_data


class SemanticRelationInline(nested_admin.NestedTabularInline):
    readonly_fields = ["updated_at"]
    model = SemanticRelation
    inlines = [SemanticRelatedLocalizationInline]
    fk_name = "from_object_item"
    form = SemanticRelationForm
    extra = 0

    def has_add_permission(self, request, obj=None):
        if getattr(obj, "museum", None):
            return True
        return False

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super(SemanticRelationInline, self).get_formset(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "to_object_item" and self.parent_obj:
            kwargs["queryset"] = db_field.related_model.objects.filter(
                museum=self.parent_obj.museum
            ).exclude(id=self.parent_obj.id)
        return super(SemanticRelationInline, self).formfield_for_foreignkey(
            db_field, request=request, **kwargs
        )


class SuggestedObjectInline(nested_admin.NestedTabularInline):
    fields = ("position", "suggested")
    model = SuggestedObject
    fk_name = "objectsitem"
    sortable_field_name = "position"
    extra = 0
    verbose_name_plural = (
        "Suggested Objects (use slider on the left side for changing a position)"
    )

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super(SuggestedObjectInline, self).get_formset(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "suggested" and self.parent_obj:
            kwargs["queryset"] = db_field.related_model.objects.filter(
                museum=self.parent_obj.museum
            ).exclude(id=self.parent_obj.id)
        return super(SuggestedObjectInline, self).formfield_for_foreignkey(
            db_field, request=request, **kwargs
        )

    def has_add_permission(self, request, obj=None):
        if getattr(obj, "museum", None):
            return True
        return False


class SingleLineLocalizationInline(nested_admin.NestedTabularInline):
    model = SingleLineLocalization
    readonly_fields = [
        "updated_at",
    ]
    extra = 0
    formfield_overrides = {
        models.TextField: {
            "widget": widgets.Textarea(
                attrs={"rows": 1, "cols": 80, "style": "height: 2em;"}
            )
        },
    }
    verbose_name_plural = "Localization"


class SingleLineForm(forms.ModelForm):
    multichoice = forms.MultipleChoiceField(
        choices=CHAT_MULTI_CHOICES,
        widget=widgets.SelectMultiple(
            attrs={
                "style": "width: 4em; height: 7em; min-height: 70px;",
                "class": "multiple-choice",
            }
        ),
        help_text='Hold down "Shift", or "Command" '
        "on a Mac, to select more than one.",
        required=False,
    )

    class Meta:
        model = SingleLine
        fields = "__all__"


class SingleLineInline(nested_admin.NestedTabularInline):
    model = SingleLine
    form = SingleLineForm
    sortable_field_name = "position"
    readonly_fields = [
        "updated_at",
    ]
    inlines = [
        SingleLineLocalizationInline,
    ]
    extra = 0
    verbose_name_plural = "Line"


class ChatDesignerInline(nested_admin.NestedTabularInline):
    model = ChatDesigner
    # fields = ('position', 'suggested')
    # fk_name = 'objectsitem'
    extra = 0
    verbose_name_plural = (
        "Chat Designer (use slider on the left side for changing a position)"
    )
    readonly_fields = [
        "updated_at",
    ]
    inlines = [
        SingleLineInline,
    ]


class ObjectsItemAdmin(nested_admin.NestedModelAdmin):
    fieldsets = (
        (
            "General Info",
            {
                "fields": (
                    "museum",
                    "floor",
                    "language_style",
                    "priority",
                    "positionx",
                    "positiony",
                    "object_level",
                    "in_tensor_model",
                    "onboarding",
                    "vip",
                ),
            },
        ),
        ("Author", {"fields": (("author"),), "classes": ("author",)}),
        (
            "Object Avatars",
            {
                "fields": (
                    "avatar",
                    "cropped_avatar",
                ),
            },
        ),
    )

    change_form_template = "admin/main/objectsitem/bulk_images.html"
    list_display = (
        "id",
        "title",
        "museum",
        "categories",
        "localizations",
        "tensor_images_number",
        "in_tensor_model",
        "images_number",
        "onboarding",
        "vip",
        "object_level",
        "sync_id",
        "updated_at",
        "avatar_id",
        "chat",
    )
    inlines = [
        SuggestedObjectInline,
        SemanticRelationInline,
        ObjectsLocalizationsInline,
        ObjectsImagesInline,
        ObjectsCategoriesInline,
        ObjectsMapInline,
        ChatDesignerInline,
        ObjectsTensorImageInline,
    ]
    readonly_fields = ["updated_at", "in_tensor_model"]
    exclude = ("synced",)
    ordering = ("-created_at",)
    list_filter = (
        ("museum", RelatedDropdownFilter),
        ("in_tensor_model", DropdownFilter),
        ("vip", DropdownFilter),
        ("onboarding", DropdownFilter),
    )

    class Media:
        js = (
            "js/jquery-3.3.1.js",
            "js/toggles_on_objectsitem.js",
        )

    def get_readonly_fields(self, request, obj=None):
        # disable musem field if object was saved
        readonly_fields = super(ObjectsItemAdmin, self).get_readonly_fields(
            request, obj
        )
        if obj:
            return readonly_fields + ["museum"]

        messages.warning(
            request,
            "Pay attention that you won't be able to change museum of the object \
                            after object was saved. Make a new object instead",
        )
        return readonly_fields

    def save_model(self, request, obj, form, change):
        # bulk images validation
        sizes = [
            True
            for file in request.FILES.getlist("photos_multiple")
            if MIN_TENSOR_IMAGE_SIZE > file.size > MAX_TENSOR_IMAGE_SIZE
        ]
        exts = [
            True
            for file in request.FILES.getlist("photos_multiple")
            if file.name.split(".")[-1] not in ["jpg", "jpeg", "JPG", "JPEG"]
        ]

        if len(
            request.FILES.getlist("photos_multiple")
        ) > settings.TENSORFLOW_BULK_UPLOAD_LIMIT or any(sizes):
            messages.warning(
                request,
                "Images number should not exceed 10 for one time and images size must be \
                                        more than 0.1 and not lareger than 3 MB each.",
            )
            return HttpResponseRedirect(".")

        if any(exts):
            list(messages.get_messages(request))
            messages.warning(
                request,
                "All tensor imags must be either one of extension 'jpg', 'jpeg', 'JPG', 'JPEG' ",
            )
            return HttpResponseRedirect(".")

        for afile in request.FILES.getlist("photos_multiple"):
            obj.object_tensor_image.create(image=afile)

        if not getattr(obj, "object_map", None):
            messages.warning(
                request,
                "For objects Map been \
                autocreated you should add Museum Map for every museum floor \
                and a pointer image with corresponding image type",
            )

        # create objects map
        museum = obj.museum
        mus_map = museum.museumsimages_set.filter(image_type=f"{obj.floor}_map")
        mus_pointer = museum.museumsimages_set.filter(image_type="pnt")

        obj.save()

        if mus_map and mus_pointer:
            if getattr(mus_map[0], "image", None) and getattr(
                mus_pointer[0], "image", None
            ):
                try:
                    mus_image = Image.open(mus_map[0].image)
                    pnt_image = Image.open(mus_pointer[0].image)
                except:
                    messages.warning(
                        request,
                        "Map autogeneration failed. \
                            Please check if museum maps images for each floor and a pointer image are available.",
                    )
                else:
                    pnt_image = pnt_image.resize((40, 40)).convert("RGBA")
                    mus_image.paste(
                        pnt_image,
                        (int(obj.positionx), int(obj.positiony)),
                        pnt_image.split()[3],
                    )

                    image_buffer = BytesIO()
                    mus_image.convert(mode="RGB").save(
                        image_buffer, "PNG", optimize=True
                    )

                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(image_buffer.getvalue())

                    obj.object_map.all().delete()
                    obj.save()
                    om = ObjectsMap()
                    om.objects_item = obj
                    om.image.save(f"o_maps/{str(obj.sync_id)}/map.png", img_temp)

        else:
            messages.warning(
                request,
                "Map autogeneration failed. \
                Please check if museum maps images for each floor and a pointer image are available.",
            )

    def avatar_id(self, obj):
        avatar = getattr(obj, "avatar", None)
        if avatar:
            return avatar.name.split("/")[-1][:20]

    def chat(self, obj):
        chat_labels = {True: "active", False: "draft"}
        if len(obj.chat_designer.all()) > 0:
            return list(
                map(
                    lambda x: {f"id {x.id}": chat_labels[x.active]},
                    obj.chat_designer.all(),
                )
            )
        obj_locs = obj.objectslocalizations_set.all()
        if obj_locs:
            return [i.conversation.name.split("/")[-1][:20] for i in obj_locs]

    def title(self, obj):
        obj = obj.objectslocalizations_set.first()
        title = getattr(obj, "title", None)
        if title:
            return title

    def tensor_images_number(self, obj):
        images_number = obj.object_tensor_image.count()
        return images_number

    def categories(self, obj):
        obj_cat = getattr(obj, "objectscategories", None)
        if obj_cat:
            categories = obj_cat.category.all()
            if categories:
                return [i.id for i in categories]

    def localizations(self, obj):
        obj_locs = obj.objectslocalizations_set.all()
        if obj_locs:
            return [i.language for i in obj_locs]

    def images_number(self, obj):
        return obj.objectsimages_set.count()


class CategorieslocalizationsInline(MinValidatedInlineMixIn, admin.TabularInline):
    model = Categorieslocalizations
    min_num = NUMBER_OF_LOCALIZATIONS
    extra = 0
    readonly_fields = ["updated_at"]
    exclude = ("synced",)


class CategoriesAdmin(admin.ModelAdmin):
    inlines = [CategorieslocalizationsInline]
    readonly_fields = ["updated_at"]
    exclude = ("synced",)


class UsersLanguageStylesInline(MinValidatedInlineMixIn, admin.TabularInline):
    model = UsersLanguageStyles
    min_num = NUMBER_OF_LOCALIZATIONS
    extra = 0
    readonly_fields = ["language_style", "score", "updated_at"]
    exclude = ("synced",)


class VotingsInline(admin.TabularInline):
    model = Votings
    extra = 0
    readonly_fields = ["objects_item", "vote", "updated_at", "sync_id"]
    fields = (
        "objects_item",
        "vote",
        "updated_at",
        "sync_id",
    )
    exclude = ("synced",)


class CollectionsInline(admin.TabularInline):
    model = Collections
    extra = 0
    readonly_fields = ["objects_item", "category", "image", "updated_at", "sync_id"]
    fields = (
        "objects_item",
        "category",
        "image",
        "updated_at",
        "sync_id",
    )
    exclude = ("synced",)


class ChatsInline(admin.TabularInline):
    model = Chats
    extra = 0
    readonly_fields = [
        "objects_item",
        "last_step",
        "history",
        "finished",
        "planned",
        "updated_at",
        "sync_id",
    ]
    fields = (
        "objects_item",
        "last_step",
        "history",
        "finished",
        "planned",
        "updated_at",
        "sync_id",
    )
    exclude = ("synced",)


class UserTourInline(admin.TabularInline):
    model = UserTour
    extra = 0
    readonly_fields = ["museum_tour", "updated_at", "sync_id"]
    fields = (
        "museum_tour",
        "updated_at",
        "sync_id",
    )
    exclude = ("synced",)


class UsersAdmin(admin.ModelAdmin):
    inlines = [
        UsersLanguageStylesInline,
        VotingsInline,
        CollectionsInline,
        ChatsInline,
        UserTourInline,
    ]
    list_display = [
        "name",
        "device_id",
        "user_level",
        "language",
        "updated_at",
        "sync_id",
    ]
    readonly_fields = [
        "name",
        "avatar",
        "device_id",
        "category",
        "positionx",
        "positiony",
        "floor",
        "font_size",
        "user_level",
        "language",
        "updated_at",
    ]
    exclude = ("synced",)


class VotingsAdmin(admin.ModelAdmin):
    model = Votings
    readonly_fields = ["updated_at"]
    exclude = ("synced",)


admin.site.register(Users, UsersAdmin)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(Museums, MuseumsAdmin)
admin.site.register(ObjectsItem, ObjectsItemAdmin)
admin.site.register(Categories, CategoriesAdmin)
