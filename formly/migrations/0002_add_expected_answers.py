# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formly', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='expected_answers',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='field',
            name='field_type',
            field=models.IntegerField(choices=[(0, b'Free Response - One Line'), (1, b'Free Response - Box'), (2, b'Multiple Choice - Pick One'), (4, b'Multiple Choice - Pick One (Dropdown)'), (5, b'Multiple Choice - Can select multiple answers'), (3, b'Date'), (6, b'File Upload'), (7, b'True/False'), (8, b'Multiple Free Response - Single Lines')]),
        ),
    ]
