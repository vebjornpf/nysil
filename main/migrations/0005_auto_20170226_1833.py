# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-26 18:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20170221_0921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise_page',
            name='youtube_url',
        ),
        migrations.AddField(
            model_name='exercise_page',
            name='youtube_id',
            field=models.CharField(default=0, max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exercise_page',
            name='explanation',
            field=models.TextField(max_length=150),
        ),
    ]