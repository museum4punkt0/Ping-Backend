# Generated by Django 2.1.7 on 2019-03-22 10:19

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_auto_20190321_1710'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='position_score',
        ),
        migrations.AlterField(
            model_name='museums',
            name='settings',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Settings'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='category_score',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
    ]
