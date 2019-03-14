# Generated by Django 2.1.7 on 2019-03-08 10:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_chats'),
    ]

    operations = [
        migrations.CreateModel(
            name='MuseumsImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=main.models.get_image_path)),
                ('image_type', models.CharField(max_length=45)),
                ('sync_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('synced', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('museum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Museums')),
            ],
        ),
    ]
