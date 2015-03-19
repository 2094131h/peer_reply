# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 1, 19, 252000), editable=False)),
                ('modified', models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 1, 19, 252000))),
                ('body', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('is_best', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField(unique=True)),
                ('created', models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 1, 19, 239000), editable=False)),
                ('modified', models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 1, 19, 239000))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 1, 19, 237000), editable=False)),
                ('modified', models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 1, 19, 237000))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LevelName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 1, 19, 248000), editable=False)),
                ('modified', models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 1, 19, 248000))),
                ('title', models.CharField(unique=True, max_length=128)),
                ('body', models.TextField()),
                ('views', models.IntegerField(default=0)),
                ('slug', models.SlugField()),
                ('course', models.ForeignKey(to='peer_reply.Course')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 1, 19, 255000), editable=False)),
                ('modified', models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 1, 19, 255000))),
                ('name', models.CharField(unique=True, max_length=60)),
                ('likes', models.IntegerField(default=0)),
                ('slug', models.SlugField(unique=True)),
                ('course', models.ForeignKey(to='peer_reply.Course')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuizAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('answer_string', models.TextField()),
                ('correct_answer', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 1, 19, 258000), editable=False)),
                ('modified', models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 1, 19, 258000))),
                ('question_string', models.TextField()),
                ('quiz', models.ForeignKey(to='peer_reply.Quiz')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('created', models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 1, 19, 233000), editable=False)),
                ('modified', models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 1, 19, 233000))),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('location', models.CharField(max_length=128)),
                ('created', models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 1, 19, 229000), editable=False)),
                ('modified', models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 1, 19, 230000))),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 1, 19, 242000), editable=False)),
                ('modified', models.DateTimeField(default=datetime.datetime(2015, 3, 19, 17, 1, 19, 242000))),
                ('username', models.CharField(max_length=60)),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('location', models.CharField(max_length=20)),
                ('no_best_answers', models.IntegerField(default=0)),
                ('no_quiz_likes', models.IntegerField(default=0)),
                ('courses', models.ManyToManyField(to='peer_reply.Course')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='school',
            name='university',
            field=models.ForeignKey(to='peer_reply.University'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quizanswer',
            name='question',
            field=models.ForeignKey(to='peer_reply.QuizQuestion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='level',
            name='name',
            field=models.ForeignKey(to='peer_reply.LevelName'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='level',
            name='school',
            field=models.ForeignKey(to='peer_reply.School'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='level',
            field=models.ForeignKey(to='peer_reply.Level'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='peer_reply.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
