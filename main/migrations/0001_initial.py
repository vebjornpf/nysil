# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 17:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_number', models.IntegerField(default=0)),
                ('chapter_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise_Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('youtube_id', models.CharField(max_length=40)),
                ('headline', models.CharField(max_length=30)),
                ('explanation', models.TextField(max_length=150)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Chapter')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('subject_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('subject_name', models.CharField(max_length=30)),
                ('professor_firstname', models.CharField(max_length=30)),
                ('professor_lastname', models.CharField(max_length=30)),
                ('professor_email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Subject'),
        ),
    ]
