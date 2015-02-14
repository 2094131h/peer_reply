from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class University(models.Model):
    name = models.CharField(max_length=128, unique=True)
    location = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(University, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=128)
    university = models.ForeignKey(University)
    slug = models.SlugField(unique=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(School, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=128, unique=False)
    school = models.ForeignKey(School)

    def __unicode__(self):
        return self.name

# class School_Level(models.Model):
#     level = models.ForeignKey(Level)
#     school = models.ForeignKey(School)


class Course(models.Model):
    name = models.CharField(max_length=128, unique=False)
    level = models.ForeignKey(Level)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    forename = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.EmailField()
    is_valid = models.BooleanField(default=False)
    location = models.CharField(max_length=20)
    no_best_answers = models.IntegerField(default=0)
    no_quiz_likes = models.IntegerField(default=0)
    courses = models.ManyToManyField(Course)
    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


class Enrolled(models.Model):
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)


class Question(models.Model):
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=128)
    body = models.CharField(max_length=3000)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    body = models.CharField(max_length=3000)
    likes = models.IntegerField()
    isBest = models.BooleanField(default=False)

    def __unicode__(self):
        return self.body


class QuizQuestion(models.Model):
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=128)
    body = models.CharField(max_length=1000)
    likes = models.IntegerField()
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(QuizQuestion, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion)
    answer_string = models.CharField(max_length=255)
    correct_answer = models.BooleanField(default=False)

    def __unicode__(self):
        return self.answer_string