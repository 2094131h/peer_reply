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

    created = models.DateTimeField(editable=False, default=datetime.datetime.today())
    modified = models.DateTimeField(default=datetime.datetime.today())

    # The additional attributes we wish to include.

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', default="profile_images/default-user-icon-profile.png")
    location = models.CharField(max_length=20, blank=True)
    courses = models.ManyToManyField(Course, blank=True)
    no_best_answers = models.IntegerField(default=0)
    no_quiz_likes = models.IntegerField(default=0)
    rep_points = models.IntegerField(default=0)
    rep_image = models.ImageField(default="profile_images/level1.gif")
 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        self.rep_points = (int(self.no_quiz_likes) * 2) + int(self.no_best_answers)
        if ((int(self.no_quiz_likes) * 2) + int(self.no_best_answers)) < 100:
            self.rep_image = '/media/profile_images/level1.gif'
        elif ((int(self.no_quiz_likes) * 2) + int(self.no_best_answers)) < 200:
            self.rep_image = '/media/profile_images/level2.gif'
        elif ((int(self.no_quiz_likes) * 2) + int(self.no_best_answers)) < 500:
            self.rep_image = '/media/profile_images/level3.gif'
        elif ((int(self.no_quiz_likes) * 2) + int(self.no_best_answers)) < 1000:
            self.rep_image = '/media/profile_images/level4.gif'
        elif ((int(self.no_quiz_likes) * 2) + int(self.no_best_answers)) < 2000:
            self.rep_image = '/media/profile_images/level5.gif'
        elif ((int(self.no_quiz_likes) * 2) + int(self.no_best_answers)) < 5000:
            self.rep_image = '/media/profile_images/level6.gif'
        elif ((int(self.no_quiz_likes) * 2) + int(self.no_best_answers)) < 10000:
            self.rep_image = '/media/profile_images/level7.gif'
        else:
            self.rep_image = '/media/profile_images/level2.gif'

        super(UserProfile, self).save(*args, **kwargs)

    # method for displaying list of users courses
    def display_courses(self):
        return ', '.join([ course.name for course in self.courses.all()[:5] ])


    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return unicode(self.user)

# Normal question class (not used for quiz questions!)
class Question(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=128)
    body = models.TextField()
    views = models.IntegerField(default=0)
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)

    # Create slug field for url
    slug = models.SlugField()

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
            if self.likes > 0: # if first time being created, don't allow any likes!
                self.likes = 0
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

    created = models.DateTimeField(editable=False, default=datetime.datetime.today())
    modified = models.DateTimeField(default=datetime.datetime.today())

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

