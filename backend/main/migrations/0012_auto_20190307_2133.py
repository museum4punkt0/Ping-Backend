# Generated by Django 2.1.7 on 2019-03-07 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20190307_1912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='objectscategories',
            name='category_id',
        ),
        migrations.AddField(
            model_name='objectscategories',
            name='category_id',
            field=models.ManyToManyField(to='main.Categories'),
        ),
    ]
