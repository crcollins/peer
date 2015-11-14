# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peer', '0005_review_editor'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='submitted',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
