import csv
import sys
import argparse
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from main.models import Categories, Museums, ObjectsItem, Settings, Users


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Add superuser [admin | pass]
        try:
            User.objects.create_superuser("admin", "admin@example.com", "pass")
            self.stdout.write(self.style.SUCCESS("Successfully added superuser"))
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("Superuser with these credentials already exists")
            )

        # Add categories to db
        with open("testdata/test_categories.csv", "r") as categories_file:
            categories_pks = []
            reader = csv.DictReader(categories_file)
            Categories.objects.all().delete()
            for _ in reader:
                category = Categories.objects.create()
                categories_pks.append(category.pk)
                category.save()

        # Add settings to db
        with open("testdata/test_settings.csv", "r") as settings_file:
            settings_pks = []
            reader = csv.DictReader(settings_file)
            Settings.objects.all().delete()
            for row in reader:
                settings = Settings.objects.create(**row)
                settings_pks.append(settings.pk)
                settings.save()

        # Add museums to db
        with open("testdata/test_museums.csv", "r") as museums_file:
            museum_pks = []
            reader = csv.DictReader(museums_file)
            ObjectsItem.objects.all().delete()
            Museums.objects.all().delete()
            for settings_pk, row in zip(settings_pks, reader):
                museum = Museums.objects.create(
                    settings=Settings.objects.get(pk=settings_pk), **row
                )
                museum_pks.append(museum.pk)
                museum.save()

        # Add objects to db
        with open("testdata/test_objects.csv", "r") as objects_file:
            reader = csv.DictReader(objects_file)
            for museum_pk, row in zip(museum_pks, reader):
                object = ObjectsItem.objects.create(
                    museum=Museums.objects.get(pk=museum_pk), **row
                )
                object.save()

        # Add users to db
        with open("testdata/test_users.csv", "r") as users_file:
            reader = csv.DictReader(users_file)
            for category_pk, row in zip(categories_pks, reader):
                user = Users.objects.create(
                    category=Categories.objects.get(pk=category_pk), **row
                )
                user.save()
