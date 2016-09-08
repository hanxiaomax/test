# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-07 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rewords', '0009_learninglist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='words',
            name='is_cet4',
        ),
        migrations.RemoveField(
            model_name='words',
            name='is_cet6',
        ),
        migrations.RemoveField(
            model_name='words',
            name='is_ielts',
        ),
        migrations.RemoveField(
            model_name='words',
            name='is_toefl',
        ),
        migrations.AddField(
            model_name='words',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]