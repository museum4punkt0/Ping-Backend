# Generated by Django 2.1.7 on 2019-03-26 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0047_auto_20190326_1617'),
    ]

    operations = [
        migrations.RenameField(
            model_name='objectsmap',
            old_name='object_map',
            new_name='image',
        ),
    ]
