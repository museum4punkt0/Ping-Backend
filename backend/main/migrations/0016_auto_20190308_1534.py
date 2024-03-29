# Generated by Django 2.1.7 on 2019-03-08 15:34

from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_museumsimages'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectsImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=main.models.get_image_path)),
                ('objects_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.ObjectsItem')),
            ],
        ),
        migrations.AlterModelOptions(
            name='categories',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='categorieslocalizations',
            options={'verbose_name_plural': 'Categorieslocalizations'},
        ),
        migrations.AlterModelOptions(
            name='chats',
            options={'verbose_name_plural': 'Chats'},
        ),
        migrations.AlterModelOptions(
            name='objectscategories',
            options={'verbose_name_plural': 'ObjectsCategories'},
        ),
        migrations.AlterField(
            model_name='collections',
            name='image',
            field=models.ImageField(blank=True, max_length=110, null=True, upload_to=main.models.get_image_path),
        ),
    ]
