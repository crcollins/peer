# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peer', '0011_paper_split_revision'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paper',
            name='pdf_file',
        ),
    ]
