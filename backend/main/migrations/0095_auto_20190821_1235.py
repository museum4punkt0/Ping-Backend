# Generated by Django 2.1.7 on 2019-08-21 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0094_auto_20190813_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertour',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_tours', related_query_name='user_tours', to='main.Users'),
        ),
    ]
