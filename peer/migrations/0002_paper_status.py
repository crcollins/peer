# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'Pending'), (1, b'Rejected'), (2, b'Revision'), (3, b'Accepted')]),
        ),
    ]
