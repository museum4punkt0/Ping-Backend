# Generated by Django 2.1.7 on 2019-05-14 15:08
from django.contrib.postgres.operations import CreateExtension
import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0072_objectsimages_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='museums',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
    ]
