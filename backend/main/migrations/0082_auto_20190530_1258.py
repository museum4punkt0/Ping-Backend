# Generated by Django 2.1.7 on 2019-05-30 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0081_semanticrelation_sync_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='museums',
            name='museum_site_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='settings',
            name='site_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
