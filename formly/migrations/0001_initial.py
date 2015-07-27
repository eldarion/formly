# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=100)),
                ('field_type', models.IntegerField(choices=[(0, b'Free Response - One Line'), (1, b'Free Response - Box'), (2, b'Multiple Choice - Pick One'), (4, b'Multiple Choice - Pick One (Dropdown)'), (5, b'Multiple Choice - Can select multiple answers'), (3, b'Date'), (6, b'File Upload'), (7, b'True/False')])),
                ('help_text', models.CharField(max_length=255, blank=True)),
                ('ordinal', models.IntegerField()),
                ('maximum_choices', models.IntegerField(null=True, blank=True)),
                ('required', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['ordinal'],
            },
        ),
        migrations.CreateModel(
            name='FieldChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=100)),
                ('field', models.ForeignKey(related_name='choices', to='formly.Field')),
                ('target', models.ForeignKey(related_name='target_choices', blank=True, to='formly.Field', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FieldResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upload', models.FileField(upload_to=b'formly/', blank=True)),
                ('answer', jsonfield.fields.JSONField(default=dict, blank=True)),
            ],
            options={
                'ordering': ['result', 'question'],
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_num', models.PositiveIntegerField(null=True, blank=True)),
                ('subtitle', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'ordering': ['survey', 'page_num'],
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('published', models.DateTimeField(null=True, blank=True)),
                ('creator', models.ForeignKey(related_name='surveys', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_submitted', models.DateTimeField(default=django.utils.timezone.now)),
                ('survey', models.ForeignKey(related_name='survey_results', to='formly.Survey')),
                ('user', models.ForeignKey(related_name='survey_results', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='survey',
            field=models.ForeignKey(related_name='pages', to='formly.Survey'),
        ),
        migrations.AddField(
            model_name='page',
            name='target',
            field=models.ForeignKey(blank=True, to='formly.Page', null=True),
        ),
        migrations.AddField(
            model_name='fieldresult',
            name='page',
            field=models.ForeignKey(related_name='results', to='formly.Page'),
        ),
        migrations.AddField(
            model_name='fieldresult',
            name='question',
            field=models.ForeignKey(related_name='results', to='formly.Field'),
        ),
        migrations.AddField(
            model_name='fieldresult',
            name='result',
            field=models.ForeignKey(related_name='results', to='formly.SurveyResult'),
        ),
        migrations.AddField(
            model_name='fieldresult',
            name='survey',
            field=models.ForeignKey(related_name='results', to='formly.Survey'),
        ),
        migrations.AddField(
            model_name='field',
            name='page',
            field=models.ForeignKey(related_name='fields', blank=True, to='formly.Page', null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='survey',
            field=models.ForeignKey(related_name='fields', to='formly.Survey'),
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('survey', 'page_num')]),
        ),
    ]
