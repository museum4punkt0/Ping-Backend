# Generated by Django 2.1.7 on 2020-03-13 13:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0113_auto_20200313_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='SingleLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(default=0)),
                ('line_type', models.CharField(choices=[('redirect', 'Redirect'), ('multichoice', 'Multichoice'), ('||Exit', 'Exit'), ('||Cam', 'Cam'), ('||Map', 'Map'), ('||Collection', 'Collection'), ('||Map', 'Map'), ('||Image1', 'Image1'), ('||Image2', 'Image2'), ('||Image3', 'Image3')], default='redirect', max_length=45)),
                ('redirect', models.PositiveIntegerField(default=0)),
                ('multichoice', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49), (50, 50), (51, 51), (52, 52), (53, 53), (54, 54), (55, 55), (56, 56), (57, 57), (58, 58), (59, 59), (60, 60), (61, 61), (62, 62), (63, 63), (64, 64), (65, 65), (66, 66), (67, 67), (68, 68), (69, 69), (70, 70), (71, 71), (72, 72), (73, 73), (74, 74), (75, 75), (76, 76), (77, 77), (78, 78), (79, 79), (80, 80), (81, 81), (82, 82), (83, 83), (84, 84), (85, 85), (86, 86), (87, 87), (88, 88), (89, 89), (90, 90), (91, 91), (92, 92), (93, 93), (94, 94), (95, 95), (96, 96), (97, 97), (98, 98), (99, 99)], max_length=287, null=True, verbose_name='Multichoices')),
                ('sync_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='single_line', to='main.ChatDesigner')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='SingleLineLocalization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('en', 'English'), ('de', 'German')], default='en', max_length=45)),
                ('text', models.TextField(blank=True, null=True)),
                ('sync_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.SingleLine')),
            ],
        ),
    ]