# Generated by Django 2.1.7 on 2019-09-15 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0098_auto_20190915_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objectsitem',
            name='author',
            field=models.CharField(blank=True, max_length=145, null=True),
        ),
        migrations.AlterField(
            model_name='objectsitem',
            name='vip',
            field=models.BooleanField(default=False),
        ),
    ]
