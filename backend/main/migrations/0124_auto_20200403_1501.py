# Generated by Django 2.1.7 on 2020-04-03 12:01

import django.core.validators
from django.db import migrations, models
import main.models
import multiselectfield.db.fields
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0123_auto_20200325_1616'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='semanticrelationlocalization',
            options={'verbose_name_plural': 'Semantic relation Localizations'},
        ),
        migrations.AlterField(
            model_name='collections',
            name='image',
            field=models.ImageField(max_length=150, upload_to=''),
        ),
        migrations.AlterField(
            model_name='musemstensor',
            name='mobile_tensor_flow_lables',
            field=models.FileField(blank=True, max_length=150, null=True, upload_to='tensor_label/'),
        ),
        migrations.AlterField(
            model_name='musemstensor',
            name='mobile_tensor_flow_model',
            field=models.FileField(blank=True, max_length=150, null=True, upload_to='tensor_model/'),
        ),
        migrations.AlterField(
            model_name='musemstensor',
            name='tensor_flow_lables',
            field=models.FileField(blank=True, max_length=150, null=True, upload_to='tensor_label/'),
        ),
        migrations.AlterField(
            model_name='musemstensor',
            name='tensor_flow_model',
            field=models.FileField(blank=True, max_length=150, null=True, upload_to='tensor_model/'),
        ),
        migrations.AlterField(
            model_name='museumsimages',
            name='image',
            field=models.ImageField(max_length=150, upload_to=main.models.get_image_path),
        ),
        migrations.AlterField(
            model_name='objectsitem',
            name='avatar',
            field=models.ImageField(blank=True, max_length=150, null=True, upload_to=main.models.get_image_path, verbose_name='full_image'),
        ),
        migrations.AlterField(
            model_name='objectsitem',
            name='cropped_avatar',
            field=models.ImageField(blank=True, max_length=150, null=True, upload_to=main.models.get_image_path, verbose_name='detail_image'),
        ),
        migrations.AlterField(
            model_name='objectslocalizations',
            name='conversation',
            field=models.FileField(blank=True, max_length=150, null=True, upload_to=main.models.get_image_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['txt'])]),
        ),
        migrations.AlterField(
            model_name='objectstensorimage',
            name='image',
            field=models.ImageField(max_length=150, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='mein-objekt-tensorflow'), upload_to=main.models.get_tensor_image_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'JPG', 'JPEG'])]),
        ),
        migrations.AlterField(
            model_name='openningtime',
            name='weekday',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('suturday', 'Saturday'), ('sunday', 'Sunday')], max_length=150),
        ),
        migrations.AlterField(
            model_name='predefinedavatars',
            name='image',
            field=models.ImageField(blank=True, max_length=150, null=True, upload_to=main.models.get_image_path),
        ),
    ]