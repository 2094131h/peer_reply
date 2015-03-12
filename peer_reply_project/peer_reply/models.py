from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class University(models.Model):
    name = models.CharField(max_length=128, unique=True)
    location = models.CharField(max_length=128)

    # Create slug field for url
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(University, self).save(*args, **kwargs)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=128)
    university = models.ForeignKey(University)

    def display_levels(self):
        return ', '.join([level.name for level in self.level_set.all()[:5]])

    slug = models.SlugField(unique=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(School, self).save(*args, **kwargs)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=128, unique=False)
    school = models.ForeignKey(School)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=128, unique=False)
    level = models.ForeignKey(Level)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

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
    title = models.CharField(max_length=128)
    body = models.TextField()
    views = models.IntegerField(default=0)
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)
    slug = models.SlugField(unique=True)

    # Create slug field for url
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.title


class Answer(models.Model):
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
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=60,unique=True)
    likes = models.IntegerField(default=0)

    # Create slug field for url
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Quiz, self).save(*args, **kwargs)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.name


class QuizQuestion(models.Model):
    question_string = models.TextField()
    quiz = models.ForeignKey(Quiz)

    def display_answers(self):
        return ', '.join([quiz_answer.answer_string for quiz_answer in self.quizanswer_set.all()[:5]])
    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.question_string


class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion)
    answer_string = models.TextField()
    correct_answer = models.BooleanField(default=False)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.answer_string

