# Generated by Django 2.1.7 on 2020-03-23 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0118_auto_20200320_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='singleline',
            name='poll',
            field=models.BooleanField(default=False),
        ),
    ]
