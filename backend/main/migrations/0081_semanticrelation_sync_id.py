# Generated by Django 2.1.7 on 2019-05-30 08:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0080_semanticrelationlocalization_sync_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='semanticrelation',
            name='sync_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
