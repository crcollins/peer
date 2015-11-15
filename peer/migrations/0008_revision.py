# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peer', '0007_paper_hash_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='Revision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comments', models.TextField(max_length=1048576)),
                ('pdf_file', models.FileField(upload_to=b'papers')),
                ('submitted', models.DateTimeField(auto_now=True)),
                ('paper', models.ForeignKey(related_name='revisions', to='peer.Paper')),
            ],
        ),
    ]
