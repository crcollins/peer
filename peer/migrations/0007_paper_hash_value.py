# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peer', '0006_review_submitted'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='hash_value',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
