# Generated by Django 2.1.7 on 2019-05-23 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0072_objectsimages_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='SemanticRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description_en', models.CharField(blank=True, max_length=100, null=True)),
                ('description_de', models.CharField(blank=True, max_length=100, null=True)),
                ('from_object_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_object_item', to='main.ObjectsItem')),
                ('to_object_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_object_item', to='main.ObjectsItem')),
            ],
        ),
        migrations.AddField(
            model_name='objectsitem',
            name='semantic_relation',
            field=models.ManyToManyField(through='main.SemanticRelation', to='main.ObjectsItem'),
        ),
    ]