# Generated by Django 2.1.7 on 2019-03-20 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_auto_20190320_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorieslocalizations',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Categories'),
        ),
    ]