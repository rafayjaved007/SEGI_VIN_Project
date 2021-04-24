# Generated by Django 3.0.3 on 2020-03-18 23:38

from django.db import migrations

from accounts.models import User


def forwards_func(apps, schema_editor):
    # build the user you now have access to via Django magic
    User.objects.create_superuser('wadood', 'wadoodislam@gmail.com', 'desimagoosh')


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func),
    ]