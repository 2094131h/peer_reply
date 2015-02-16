import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peer_reply_project.settings')
from peer_reply.models import Course, School, Level, University, Question, Answer, QuizQuestion, QuizAnswer
import django

django.setup()


def populate():
    python_university = add_university('University of Glasgow', 'Glasgow')

    python_school = 0;
    python_level = 0;
    count = 0
    school_count = 0


    # loop through each line in glasgow uni data file and add data to database
    with open('glasgow_uni_data.txt', 'r') as f:
        for line in f:
            # if line starts with ';' then it is a school name so create new school
            if line.startswith(';'):
                python_school = add_school(line[1:], python_university)
            # only add levels and courses to first 15 schools during development (to save time)
            elif line.startswith('Level') and school_count <= 15:
                python_level = add_level(line, python_school)
            elif count < 12 and school_count <= 15:
                add_course(line, python_level)


def add_question(course, user, title, body):
    q = Question.object.get_or_create(course=course, user=user, title=title, body=body)
    return q


def add_answer(question, user, body):
    a = Answer.object.get_or_create(question=question, user=user, body=body)
    return a


def add_quiz(course, user, name):
    qz = Quiz.object.get_or_create(course=course, user=user, name=name)
    return qz


def add_quiz_question(course, user, title, body, quiz):
    qq = QuizQuestion.object.get_or_create(course=course, user=user, title=title, body=body, quiz=quiz)
    return qq


def add_university(name, location):
    u = University.objects.get_or_create(name=name, location=location)[0]
    return u


def add_school(name, university):
    s = School.objects.get_or_create(name=name, university=university)[0]
    return s


def add_level(name, school):
    l = Level.objects.get_or_create(name=name, school=school)[0]
    return l


def add_course(name, level):
    c = Course.objects.get_or_create(name=name, level=level)[0]
    c.save()
    return c


# Start execution here!
if __name__ == '__main__':
    print "Starting Peer Reply population script..."
    populate()
    print "Finished populating database"
