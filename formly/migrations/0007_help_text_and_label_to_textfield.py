# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-11 16:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formly', '0006_auto_20161206_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='help_text',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='label',
            field=models.TextField(),
        ),
    ]
