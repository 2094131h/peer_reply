from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


import datetime

class University(models.Model):
    name = models.CharField(max_length=128, unique=True)
    location = models.CharField(max_length=128)

    created = models.DateTimeField(editable=False,default=datetime.datetime.today())
    modified = models.DateTimeField(default=datetime.datetime.today())

    # Create slug field for url
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        super(University, self).save(*args, **kwargs)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=128)
    university = models.ForeignKey(University)

    created = models.DateTimeField(editable=False,default=datetime.datetime.today())
    modified = models.DateTimeField(default=datetime.datetime.today())

    def display_levels(self):
        return ', '.join([level.name for level in self.level_set.all()[:5]])

    slug = models.SlugField(unique=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        super(School, self).save(*args, **kwargs)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.name

class LevelName(models.Model):
    name = models.CharField(max_length=128, unique=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.name


class Level(models.Model):
    name = models.ForeignKey(LevelName)
    school = models.ForeignKey(School)
    created = models.DateTimeField(editable=False,default=datetime.datetime.today())
    modified = models.DateTimeField(default=datetime.datetime.today())

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        # On save, update timestamps
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        super(Level, self).save(*args, **kwargs)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=128, unique=False)
    level = models.ForeignKey(Level)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
    created = models.DateTimeField(editable=False,default=datetime.datetime.today())
    modified = models.DateTimeField(default=datetime.datetime.today())

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        # On save, update timestamps
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        super(Course, self).save(*args, **kwargs)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    created = models.DateTimeField(editable=False,default=datetime.datetime.today())
    modified = models.DateTimeField(default=datetime.datetime.today())

    # The additional attributes we wish to include.
    username = models.CharField(max_length=60, unique=False)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    location = models.CharField(max_length=20)
    courses = models.ManyToManyField(Course)
    no_best_answers = models.IntegerField(default=0)
    no_quiz_likes = models.IntegerField(default=0)

    # method for displaying list of users courses
    def display_courses(self):
        return ', '.join([ course.name for course in self.courses.all()[:5] ])


    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.username

# Normal question class (not used for quiz questions!)
class Question(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=128, unique=True)
    body = models.TextField()
    views = models.IntegerField(default=0)
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)

    # Create slug field for url
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        # On save, update timestamps
        if not self.id:
            self.created = datetime.datetime.today()
        # correct wrong input
        if self.views < 0:
            self.views = 0
        self.modified = datetime.datetime.today()
        super(Question, self).save(*args, **kwargs)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.title


class Answer(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    flags = models.IntegerField(default=0)
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    body = models.TextField()
    likes = models.IntegerField(default=0)
    is_best = models.BooleanField(default=False)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        #return question.title + " answer"
        return self.body

class Quiz(models.Model):
    created = models.DateTimeField(editable=False,default=datetime.datetime.today())
    modified = models.DateTimeField(default=datetime.datetime.today())

    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=60,unique=True)
    likes = models.IntegerField(default=0)

    # Create slug field for url
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        super(Quiz, self).save(*args, **kwargs)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.name


class QuizQuestion(models.Model):


    created = models.DateTimeField(editable=False,default=datetime.datetime.today())
    modified = models.DateTimeField(default=datetime.datetime.today())
    question_string = models.TextField()
    quiz = models.ForeignKey(Quiz)

    def display_answers(self):
        return ', '.join([quiz_answer.answer_string for quiz_answer in self.quizanswer_set.all()[:5]])

    def save(self, *args, **kwargs):
        # On save, update timestamps
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        return super(QuizQuestion, self).save(*args, **kwargs)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.question_string


class QuizAnswer(models.Model):

    created = models.DateTimeField(editable=False,default=datetime.datetime.today())
    modified = models.DateTimeField(default=datetime.datetime.today())

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()
    question = models.ForeignKey(QuizQuestion)
    answer_string = models.TextField()
    correct_answer = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        # On save, update timestamps
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        return super(QuizAnswer, self).save(*args, **kwargs)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.answer_string

