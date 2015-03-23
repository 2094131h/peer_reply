from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from peer_reply.models import Quiz,QuizAnswer,QuizQuestion,Answer,Question
from peer_reply.models import User,Level,LevelName,School,University,Course,UserProfile

# Helper methods begin
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

def create_world():
    university = add_university('University of Glasgow','Glasgow')
    school = add_school('default_school',university)
    levelname = add_level_name('default_level')
    level = add_level(levelname,school)
    user = add_user('default','default', 'default@a.com', 'default','defaultuser')
    course = add_course('default_course', level)
    return {'university':university,'school':school,'levelname':levelname,'level':level,'user':user,'course':course}

# Helper methods end

#View Tests  
class IndexViewTests(TestCase):

    def test_index_view_with_no_questions(self):      
        """
        If no questions exist, an appropriate message should be displayed.
        """
        world = create_world()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, " ")
        

class QuestionViewTests(TestCase):
    
    def test_question_view_(self):
        """
        Checking if the page is accessible
        """
        world = create_world()
        course = world['course']
        user = world['user']
        q = Question(course=course,user=user,title='test Question',views=-1)
        q.save()
        expected_url = 'view_question/'+q.slug+'/'
        response = self.client.get(reverse('view_question', kwargs={'question_id':q.id,'question_title_slug':q.slug}))
        self.assertEqual(response.status_code,200)
    
class ProfileViewTests(TestCase):

    def test_profile_view_with_no_profile(self):
        """
        A new user doesn't have a profile, and clicking the profile button should
        redirect to add_profile view
        """
        world = create_world()
        response = self.client.get(reverse('profile', args={"defaultuser"}))
        self.assertEqual(response.status_code, 302) #redirect status code 302

class UsersViewTests(TestCase):
    
    def test_users_page(self):
        """
        Users page should have the default user in it.
        """
        world = create_world()
        user = world['user']
        response = self.client.get(reverse('user_profiles'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)

        

# Method Tests        
class QuestionMethodTests(TestCase):
   
    def test_ensure_views_are_positive(self):
        """
        ensure_views_are_positive should results True for questions where views are zero or positive
        """
        world = create_world()
        course = world['course']
        user = world['user']
        q = Question(course=course,user=user,title='test Question',views=-1)
        q.save()
        self.assertEqual((q.views >= 0), True)
        
    def test_slug_line_creation(self):
        """
        slug_line_creation checks to make sure that when we add a category an appropriate slug line is created
        i.e. "Random Category String" -> "random-category-string"
        """
        world = create_world()
        course = world['course']
        user = world['user']
        q = Question(course=course,user=user,title='test Question')
        q.save()
        self.assertEqual(q.slug, 'test-question')

class QuizMethodTests(TestCase):

    def test_ensure_quiz_starts_with_no_likes(self):
        """
        quiz should should have the default like as 0
        """
        world = create_world()
        course = world['course']
        user = world['user']
        q = Quiz(course=course,user=user,name='test Quiz', likes=2000)
        q.save()
        self.assertEqual((q.likes == 0), True)
        
    def test_slug_line_creation(self):
        """
        slug_line_creation checks to make sure that when we add a quiz an appropriate slug line is created
        i.e. "Random Category String" -> "random-category-string"
        """
        world = create_world()
        course = world['course']
        user = world['user']
        q = Quiz(course=course,user=user,name='test Quiz')
        q.save()
        self.assertEqual(q.slug, 'test-quiz')

class QuizAnswerMethodTest(TestCase):
    
    def test_ensure_foreginkey_quiz(self):
        """
        checking if the quizquestion foreign key points to the right quiz
        """
        world = create_world()
        course = world['course']
        user = world['user']
        q = Quiz(course=course,user=user,name='test Quiz')
        q.save()
        qq = QuizQuestion(quiz=q,question_string='test quiz question')
        qq.save()
        qa = QuizAnswer(question=qq,answer_string='',correct_answer='DNE')
        qa.save()
        self.assertEqual(qa.question, qq)
        
