# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peer', '0003_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='paper',
            field=models.ForeignKey(related_name='reviews', to='peer.Paper'),
        ),
    ]
