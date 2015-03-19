import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peer_reply_project.settings')
from peer_reply.models import Course, School, Level, University,Quiz, Question, Answer, QuizQuestion, QuizAnswer
from peer_reply.models import UserProfile
from peer_reply.models import UserProfile, LevelName
from django.contrib.auth.models import User
import django

django.setup()


def populate():
    python_university = add_university('University of Glasgow', 'Glasgow')

    python_school = 0;
    python_level = 0;
    course_count = 0
    school_count = 0
    quiz_count = 0

    user = add_user('Default', 'User', 'defaultuser@glasgow.ac.uk', 'password', "default_username")
    #user_profile = add_profile(user,'username', 'Glasgow')
    # loop through each line in glasgow uni data file and add data to database

    with open('glasgow_uni_data.txt', 'r') as f:
        for line in f:
            # if line starts with ';' then it is a school name so create new school
            if line.startswith(';'):
                python_school = add_school(line[1:], python_university)
                school_count += 1

            # only add levels and courses to first 15 schools during development (to save time)
            elif line.startswith('Level') and school_count <= 10:
                python_level_name = add_level_name(line)
                python_level = add_level(python_level_name, python_school)
                course_count = 0
            elif course_count < 7 and school_count <= 15:
                course_count += 1
                course = add_course(line, python_level)

                if course_count == 1:
                    user.profile.courses.add(course)
                    user.save()

                question = add_question(course, user, 'default question about ' + course.name,
                                        'Default question body text.')
                add_answer(question, user, 'Default reply to question about' + course.name, course_count)
                if course_count < 2:
                    quiz = add_quiz(course, user, "Default Quiz " + quiz_count.__str__(), course_count)
                    quiz_count += 1
                    for i in range(1, 5, 1):
                        quiz_question = add_quiz_question("Default Quiz question " + i.__str__(), quiz)
                        for j in range(1, 5, 1):
                            if j == 4:
                                quiz_answer = add_quiz_answer(quiz_question , "Default quiz answer" + j.__str__(), True)
                            else:
                                quiz_answer = add_quiz_answer(quiz_question , "Default quiz answer" + j.__str__(), False)




def add_user(fname, lname, email, password, username):
    u = User.objects.create_user(first_name=fname,last_name=lname, email=email, password=password,username=username)
    UserProfile.objects.get_or_create(user=u )[0]
    u.last_name = lname
    u.save
    return u


def add_question(course, user, title, body):
    q = Question.objects.get_or_create(course=course, user=user, title=title, body=body)[0]
    return q


def add_answer(question, user, body, likes):
    a = Answer.objects.get_or_create(question=question, user=user, body=body, likes=likes)[0]
    return a


def add_quiz(course, user, name, likes):
    qz = Quiz.objects.get_or_create(course=course, user=user, name=name, likes=likes)[0]
    return qz


def add_quiz_question( body, quiz):
    qq = QuizQuestion.objects.get_or_create(question_string=body, quiz=quiz)[0]
    return qq

def add_quiz_answer(question, answer_string, correct_answer):
    qa = QuizAnswer.objects.get_or_create(question=question, answer_string=answer_string, correct_answer=correct_answer)[0]
    return qa


def add_university(name, location):
    u = University.objects.get_or_create(name=name, location=location)[0]
    return u


def add_school(name, university):
    s = School.objects.get_or_create(name=name, university=university)[0]
    return s


def add_level_name(name):
    ln = LevelName.objects.get_or_create(name=name)[0]
    return ln

def add_level(name, school):
    l = Level.objects.get_or_create(name=name, school=school)[0]
    return l


def add_course(name, level):
    c = Course.objects.get_or_create(name=name, level=level)[0]
    c.save()
    return c

def add_profile(user, username, location):
    profile = UserProfile.objects.get_or_create(user=user, username=username, location=location)
    return profile

# Start execution here!
if __name__ == '__main__':
    print "Starting Peer Reply population script..."
    populate()
    print "Finished populating database"
