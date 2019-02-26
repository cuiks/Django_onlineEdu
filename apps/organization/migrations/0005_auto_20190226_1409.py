# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-02-26 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_teacher_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='need_know',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='课程须知'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='teacher_tell',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='老师告诉你'),
        ),
    ]