# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models

users = (
    {
        "username": "reviewer",
        "email": "r.eviewer@test.com",
        "first_name": "Robert",
        "last_name": "Eviewer",
    },
    {
        "username": "editor",
        "email": "e.ditor@test.com",
        "first_name": "Edward",
        "last_name": "Ditor",
    },
)
#settings.AUTH_USER_MODEL

def add_users(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    
    User = apps.get_model("auth", "User")
    for user in users:
        User.objects.using(db_alias).create(**user)


def remove_users(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    User = apps.get_model("auth", "User")
    
    for user in users:
        User.objects.using(db_alias).get(**user).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('peer', '0012_paper_split_revision_2'),
    ]

    operations = [
        migrations.RunPython(add_users, remove_users), 
    ]
