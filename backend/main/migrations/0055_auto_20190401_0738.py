# Generated by Django 2.1.7 on 2019-04-01 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0054_auto_20190328_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collections',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]