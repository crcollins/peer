# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peer', '0009_auto_20151116_0132'),
    ]

    operations = [
        migrations.AddField(
            model_name='revision',
            name='hash_value',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
