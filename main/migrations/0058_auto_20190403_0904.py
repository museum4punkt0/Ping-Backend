# Generated by Django 2.1.7 on 2019-04-03 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0057_auto_20190402_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Categories'),
        ),
    ]