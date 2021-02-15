# Generated by Django 2.1.7 on 2019-03-09 16:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20190308_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectsLocalizations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(blank=True, max_length=45, null=True)),
                ('conversation', models.CharField(blank=True, max_length=45, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=45, null=True)),
                ('language_style', models.CharField(blank=True, max_length=45, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='objectsimages',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='objectsimages',
            name='sync_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='objectsimages',
            name='synced',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='objectsimages',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='museumsimages',
            name='image',
            field=models.ImageField(blank=True, max_length=110, null=True, upload_to=main.models.get_image_path),
        ),
        migrations.AlterField(
            model_name='objectsimages',
            name='image',
            field=models.ImageField(blank=True, max_length=110, null=True, upload_to=main.models.get_image_path),
        ),
        migrations.AlterField(
            model_name='objectsitem',
            name='avatar',
            field=models.ImageField(blank=True, max_length=110, null=True, upload_to=main.models.get_image_path),
        ),
        migrations.AddField(
            model_name='objectslocalizations',
            name='objects_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.ObjectsItem'),
        ),
    ]
