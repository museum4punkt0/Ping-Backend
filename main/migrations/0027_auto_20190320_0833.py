# Generated by Django 2.1.7 on 2019-03-20 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20190318_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objectscategories',
            name='category',
            field=models.ManyToManyField(default=1, to='main.Categories'),
        ),
    ]
