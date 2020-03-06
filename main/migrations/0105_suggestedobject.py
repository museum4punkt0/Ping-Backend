# Generated by Django 2.1.7 on 2020-02-24 14:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0104_auto_20200220_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuggestedObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('objectsitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggested_object', to='main.ObjectsItem')),
            ],
        ),
    ]
