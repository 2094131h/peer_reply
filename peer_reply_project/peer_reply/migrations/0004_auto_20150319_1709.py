# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('peer_reply', '0003_auto_20150319_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 9, 39, 823000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='answer',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 9, 39, 823000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 9, 39, 809000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 9, 39, 809000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='level',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 9, 39, 807000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='level',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 9, 39, 807000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 9, 39, 819000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 9, 39, 819000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quiz',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 9, 39, 826000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quiz',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 9, 39, 827000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 9, 39, 830000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 9, 39, 830000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='school',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 9, 39, 802000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='school',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 9, 39, 802000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='university',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 9, 39, 800000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='university',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 9, 39, 800000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 9, 39, 812000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 9, 39, 812000)),
            preserve_default=True,
        ),
    ]
