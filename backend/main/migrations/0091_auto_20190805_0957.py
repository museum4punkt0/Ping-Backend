# Generated by Django 2.1.7 on 2019-08-05 09:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0090_merge_20190723_0813'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectsTensorImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=110, upload_to=main.models.get_tensor_image_path)),
                ('sync_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('synced', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('objects_item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='object_tensor_image', to='main.ObjectsItem')),
            ],
            options={
                'verbose_name_plural': 'Objects Tensor Image',
            },
        ),
        migrations.AlterField(
            model_name='settings',
            name='recognition_threshold',
            field=models.SmallIntegerField(default=50, validators=[main.models.validate_percent]),
        ),
    ]
