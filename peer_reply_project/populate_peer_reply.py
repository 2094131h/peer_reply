import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peer_reply_project.settings')
from peer_reply.models import Course, School, Level, University,Quiz, Question, Answer, QuizQuestion, QuizAnswer
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

    user = add_user('Default', 'User', '1234567a@glasgow.ac.uk', 'password', "default_username")
    # user_profile = add_profile(user,'username', 'Glasgow')
    # loop through each line in glasgow uni data file and add data to database

    user1 = add_user('Harold', 'Abbott', '1234567b@glasgow.ac.uk', 'password', 'haroldabbott')
    user2 = add_user('Peter', 'Rabbit', '1234567c@glasgow.ac.uk', 'password', 'peterrabbit')
    user3 = add_user('Jenny', 'Fielding', '1234567d@glasgow.ac.uk', 'password', 'jennyfielding')
    user4 = add_user('Fredrico', 'Galleoni', '1234567e@glasgow.ac.uk', 'password', 'fredricogalleoni')
    user5 = add_user('Kleopatra', 'Ramsey', '1234567f@glasgow.ac.uk', 'password', 'kleopatraramsey')
    user6 = add_user('General', 'User', '1234567g@glasgow.ac.uk', 'test', 'test')

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

    #put a valid course-name in a variable by obtaining it from database
    exCourse1 = Course.objects.get(id=1)
    #put a title in a variable
    exTitle1 = "Assessed Exercise part 3?"
    #put a body in a variable
    exBody1 = "Does anybody know what they want in Assessed Exercise part 3?"
    # --->> create a question
    question_1 = add_question(exCourse1, user1, exTitle1, exBody1)
    ex1a = "I think they want us to just discuss the statistics from the company's point of view, and construct diagrams and graphs."
    answer_1a = add_answer(question_1, user2, ex1a, 12)
    ex1b = "Basically, do the graphs?"
    answer_1b = add_answer(question_1, user3, ex1b, 6)
    ex1c = "No idea, they're so unclear in the instructions."
    answer_1c = add_answer(question_1, user4, ex1c, 1)

    exTitle2 = "Deadline postponed for tutorial?"
    exBody2 = "Is it true that the deadline for next tutorial exercise has been postponed?"
    question_2 = add_question(exCourse1, user1, exTitle2, exBody2)
    ex2a = "yeah, since they uploaded it so late we get another 2 days."
    answer_2a = add_answer(question_2, user2, ex2a, 9)
    ex2b = "I haven't heard about it."
    answer_2b = add_answer(question_2, user3, ex2b, 1)
    ex2c = "+2 days"
    answer_2c = add_answer(question_2, user4, ex2c, 4)

    exTitle3 = "Revision advice?"
    exBody3 = "Thinking about starting revision now. What do you think I should focus on?"
    question_3 = add_question(exCourse1, user2, exTitle3, exBody3)
    ex3a = "i would simply read through slides, memorise definitions, and do the textbook exercises."
    answer_3a = add_answer(question_3, user1, ex3a, 20)
    ex3b = "Yeah, but tutorial sheets have a really nice selection of problems, similar to past exams."
    answer_3b = add_answer(question_3, user3, ex3b, 17)
    ex3c = "If your time is limited i suppose reviewing tutorial sheets is the smartest study strategy."
    answer_3c = add_answer(question_3, user4, ex3c, 15)

    exTitle4 = "Group project"
    exBody4 = "Does anyone need a member in their group project team? Missed last tutorial:( :("
    question_4 = add_question(exCourse1, user1, exTitle4, exBody4)
    ex4a = "We are only 3 in ours, so I suppose you can join us. We're group C5, I believe."
    answer_4a = add_answer(question_4, user2, ex4a, 13)
    ex4b = "I have heard of other group-less people. Maybe you can form a group together?"
    answer_4b = add_answer(question_4, user3, ex4b, 10)
    ex4c = "lol"
    answer_4c = add_answer(question_4, user4, ex4c, 2)

    ####Test data for different courses
    exCourse2 = Course.objects.get(id=2)
    exTitle5 = "Equations and stuff"
    exBody5 = "Could anyone please explain how the equation on p. 230 in the textbook works?"
    question_5 = add_question(exCourse2, user3, exTitle5, exBody5)
    ex5a = "Check out the last slideshow on Moodle. It has a really good explanation!"
    answer_5a = add_answer(question_5, user2, ex5a, 14)
    ex5b = "Try google"
    answer_5b = add_answer(question_5, user1, ex5b, 2)

    exCourse3 = Course.objects.get(id=3)
    exTitle6 = "Discussion section points"
    exBody6 = "What points do you suggest I bring up for the discussion section?"
    question_6 = add_question(exCourse3, user1, exTitle6, exBody6)
    ex6a = "go for the usual: validity, reliability, possible extensions/confounds."
    answer_6a = add_answer( question_6, user2, ex6a, 19)
    ex6b = "I brought up differences to past examples in the literature."
    answer_6b = add_answer(question_6, user3, ex6b, 10)

    exCourse4 = Course.objects.get(id=4)
    exTitle7 = "Tutorial attendance"
    exBody7 = "How many tutorials do you have to attend to pass the course?"
    question_7 = add_question( exCourse4, user2, exTitle7, exBody7)
    ex7a = "I think you're allowed to skip 2 tutorials maximum."
    answer_7a = add_answer(question_7, user1, ex7a, 9)
    ex7b = "i have heard 70% which would allow you to skip three I think?"
    answer_7b = add_answer(question_7, user3, ex7b, 11)
    ex7c = "no idea"
    answer_7c = add_answer(question_7, user4, ex7c, 1)

    exQuiz = add_quiz( exCourse1, user2, "Business quiz", 12 )
    exQuizQues1 = add_quiz_question("What is market?", exQuiz )
    exQuizAns1a = add_quiz_answer(exQuizQues1, "A place of buyers and sellers", True)
    exQuizAns1b = add_quiz_answer(exQuizQues1, "A word", False)
    exQuizAns1c = add_quiz_answer(exQuizQues1, "A square with selling booths", False)
    exQuizAns1d = add_quiz_answer(exQuizQues1, "There is no such thing", False)

    exQuizQues2 = add_quiz_question("What is business?", exQuiz)
    exQuizAns2a = add_quiz_answer(exQuizQues2, "Buying, selling and stuff", True)
    exQuizAns2b = add_quiz_answer(exQuizQues2, "A word", False)
    exQuizAns2c = add_quiz_answer(exQuizQues2, "An animal", False)
    exQuizAns2d = add_quiz_answer(exQuizQues2, "A fruit", False)


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
    profile = UserProfile.objects.get_or_create(useer=user, username=username, location=location)
    return profile

# Start execution here!
if __name__ == '__main__':
    print "Starting Peer Reply population script..."
    populate()
    print "Finished populating database"
