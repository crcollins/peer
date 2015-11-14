# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('peer', '0002_paper_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comments', models.TextField(max_length=1048576)),
                ('decision', models.IntegerField(choices=[(1, b'Rejected'), (2, b'Revision'), (3, b'Accepted')])),
                ('author', models.ForeignKey(related_name='reviews', to=settings.AUTH_USER_MODEL)),
                ('paper', models.ForeignKey(to='peer.Paper')),
            ],
        ),
    ]
