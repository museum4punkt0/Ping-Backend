# Generated by Django 2.1.7 on 2019-04-03 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0058_auto_20190403_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collections',
            name='objects_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.ObjectsItem'),
        ),
    ]
