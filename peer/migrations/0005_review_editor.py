# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peer', '0004_auto_20151114_0229'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='editor',
            field=models.BooleanField(default=False),
        ),
    ]
