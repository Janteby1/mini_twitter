# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-08 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0004_auto_20160408_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='tags',
            field=models.CharField(default=None, max_length=120, null=True),
        ),
    ]
