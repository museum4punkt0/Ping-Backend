# Generated by Django 2.1.7 on 2019-03-21 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0037_auto_20190321_1459'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='settingspredefinedobjectsitems',
            options={'verbose_name_plural': 'Predefined Objects'},
        ),
        migrations.RemoveField(
            model_name='settings',
            name='predifined_objects',
        ),
    ]
