# Generated by Django 2.1.7 on 2019-04-04 07:51

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0064_auto_20190404_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userslanguagestyles',
            name='language_style',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, max_length=145, null=True),
        ),
    ]
