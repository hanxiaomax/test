# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-30 22:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rewords', '0005_auto_20160831_0609'),
    ]

    operations = [
        migrations.RenameField(
            model_name='learninglist',
            old_name='user_id',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='learninglist',
            old_name='word_id',
            new_name='target_word',
        ),
        migrations.RenameField(
            model_name='notes',
            old_name='user_id',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='notes',
            old_name='word_id',
            new_name='target_word',
        ),
        migrations.AlterField(
            model_name='learninglist',
            name='last_time',
            field=models.DateTimeField(),
        ),
    ]
