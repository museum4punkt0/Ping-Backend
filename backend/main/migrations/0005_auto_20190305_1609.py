# Generated by Django 2.1.7 on 2019-03-05 16:09

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20190305_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='users',
            name='sync_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='users',
            name='synced',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='users',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
