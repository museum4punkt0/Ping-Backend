# Generated by Django 2.1.7 on 2019-03-20 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_auto_20190320_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userslanguagestyles',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.Users'),
        ),
    ]
