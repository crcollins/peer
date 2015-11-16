# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def split_paper_model(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Paper = apps.get_model("peer", "Paper")
    Revision = apps.get_model("peer", "Revision")
    for paper in Paper.objects.all():
        Revision.objects.using(db_alias).create(
                comments='',
                pdf_file=paper.pdf_file,
                submitted=paper.submitted,
                paper=paper,
                hash_value=paper.hash_value
        )
        

def merge_paper_model(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Paper = apps.get_model("peer", "Paper")
    Revision = apps.get_model("peer", "Revision")
    for paper in Paper.objects.all():
        try:
            rev = Revision.objects.using(db_alias).filter(paper=paper).earliest()
        except Revision.DoesNotExist:
            # log
            continue
        
        paper.pdf_file = rev.pdf_file
        paper.hash_value = rev.hash_value
        paper.save()
        rev.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('peer', '0010_revision_hash_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='pdf_file',
            field=models.FileField(upload_to='papers', null=True),
            preserve_default=False,
        ),
        migrations.RunPython(split_paper_model, merge_paper_model), 
        migrations.RemoveField(
            model_name='paper',
            name='hash_value',
        ),
    ]
