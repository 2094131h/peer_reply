# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('peer_reply', '0002_auto_20150319_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 8, 12, 18000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='answer',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 8, 12, 18000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 8, 12, 6000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 8, 12, 6000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='level',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 8, 12, 3000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='level',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 8, 12, 3000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 8, 12, 15000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 8, 12, 15000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quiz',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 8, 12, 21000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quiz',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 8, 12, 22000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 8, 12, 25000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 8, 12, 25000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='school',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 8, 11, 999000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='school',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 8, 11, 999000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='university',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 8, 11, 996000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='university',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 8, 11, 997000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 8, 12, 8000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 8, 12, 8000)),
            preserve_default=True,
        ),
    ]
