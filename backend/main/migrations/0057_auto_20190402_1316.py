# Generated by Django 2.1.7 on 2019-04-02 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0056_auto_20190402_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='users',
            name='category',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Categories'),
        ),
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='users',
            name='positionx',
            field=models.DecimalField(db_column='positionX', decimal_places=0, default=0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='users',
            name='positiony',
            field=models.DecimalField(db_column='positionY', decimal_places=0, default=0, max_digits=3),
        ),
    ]