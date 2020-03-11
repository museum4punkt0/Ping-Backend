# Generated by Django 2.1.7 on 2020-02-19 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0102_auto_20191113_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='objectsitem',
            name='object_level',
            field=models.CharField(choices=[('1', 1), ('2', 2), ('3', 3)], default=1, max_length=45),
        ),
        migrations.AddField(
            model_name='users',
            name='font_size',
            field=models.CharField(blank=True, default=None, max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='user_level',
            field=models.CharField(choices=[('1', 1), ('2', 2), ('3', 3)], default=1, max_length=45),
        ),
    ]