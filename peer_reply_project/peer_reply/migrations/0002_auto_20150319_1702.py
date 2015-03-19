# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('peer_reply', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 2, 37, 52000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='answer',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 2, 37, 52000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 2, 37, 39000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 2, 37, 39000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='level',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 2, 37, 36000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='level',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 2, 37, 36000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 2, 37, 48000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 2, 37, 48000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quiz',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 2, 37, 55000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quiz',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 2, 37, 56000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 2, 37, 58000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 2, 37, 58000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='school',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 2, 37, 32000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='school',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 2, 37, 32000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='university',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 2, 37, 30000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='university',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 2, 37, 30000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 2, 37, 42000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 2, 37, 42000)),
            preserve_default=True,
        ),
    ]
