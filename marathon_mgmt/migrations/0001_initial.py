# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-19 02:43
from __future__ import unicode_literals

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermMarathon',
            fields=[
            ],
            options={
                'permissions': (('can_add', 'Can add new app'), ('can_run', 'Can start, stop, restart app')),
                'proxy': True,
            },
            bases=('auth.permission',),
            managers=[
                ('objects', django.contrib.auth.models.PermissionManager()),
            ],
        ),
    ]