# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-02-27 10:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='birday',
            new_name='birthday',
        ),
    ]
