# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-04 12:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IoT_pki', '0004_auto_20170703_0830'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='is_ca',
            field=models.BooleanField(default=False),
        ),
    ]
