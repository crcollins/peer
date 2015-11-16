# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peer', '0008_revision'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'get_latest_by': 'submitted'},
        ),
        migrations.AlterModelOptions(
            name='revision',
            options={'get_latest_by': 'submitted'},
        ),
    ]
