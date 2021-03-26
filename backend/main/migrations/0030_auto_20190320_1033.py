# Generated by Django 2.1.7 on 2019-03-20 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_auto_20190320_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='positionx',
            field=models.DecimalField(db_column='positionX', decimal_places=8, default=0, max_digits=11),
        ),
        migrations.AlterField(
            model_name='users',
            name='positiony',
            field=models.DecimalField(db_column='positionY', decimal_places=8, default=0, max_digits=11),
        ),
    ]