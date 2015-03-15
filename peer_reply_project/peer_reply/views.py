from django.shortcuts import render
from django.http import HttpResponse
from peer_reply.models import University, School, Level, UserProfile, Question, Answer, Quiz, Course
from peer_reply.forms import CourseForm, QuestionForm
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.db.models import Q
import json


# @ensure_csrf_cookie
def index(request):
    # Query the database for the universities ordered by name

    universities = University.objects.order_by('-name')[:1]
    university = University.objects.get(slug='university-of-glasgow')
    school_list = School.objects.all().filter(university=university).order_by('-name')
    levels = Level.objects.all()

    context_dict = {'schools': school_list, 'universities': universities}

    # Render the response and send it back!
    return render(request, 'peer_reply/index.html', context_dict)

def left_block(request):

    if request.user.is_authenticated():
        user_profile = request.user.profile
        # user = User.objects.get(username=user.username)

        # userprofile = UserProfile.objects.all().filter(user=user)
        context_dict['user_profile'] = user_profile
    else:
        universities = University.objects.order_by('-name')[:1]
        university = University.objects.get(slug='university-of-glasgow')
        school_list = School.objects.all().filter(university=university).order_by('-name')
        context_dict['schools'] = School.objects.all().filter(university=university).order_by('-name')
    # Render the response and send it back!
    return render(request, 'peer_reply/left_block.html', context_dict)

def base(request):
    user = request.user
    userprofile = UserProfile.objects.get(user=user)
    return {'userprofile': userprofile, }


def course(request, course_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:


        course = Course.objects.get(slug=course_name_slug)
        context_dict['universities'] = University.objects.order_by('-name')[:1]
        context_dict['questions'] = Question.objects.all().filter(course=course).order_by('-views')[:20]

    except Course.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'peer_reply/course.html', context_dict)


def school(request, school_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:

        cur_school = School.objects.get(slug=school_name_slug)
        level_list = Level.objects.all().filter(school=cur_school).order_by('name')
        context_dict['levels'] = level_list
        context_dict['school'] = cur_school
    except School.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'peer_reply/school.html', context_dict)


def add_question(request):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}
    # if(course_name_slug ):
    #
    #     course = Course.objects.get(slug=course_name_slug)
    # else:


    # A HTTP POST?
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            if course:
                question = form.save(commit=False)
                question.course = course
                question.user = request.user
                question.save()
                # probably better to use a redirect here.
                return render(request, 'peer_reply/ask.html')
        else:

            context_dict['error'] = 'error'
            context_dict['form'] = form
            return render(request, 'peer_reply/ask.html', context_dict)

    else:
        university = University.objects.get(slug='university-of-glasgow')
        schools = School.objects.all().filter(university=university).order_by('name')
        # If the request was not a POST, display the form to enter details.
        form = QuestionForm()
        context_dict = {'form': form, 'course': course, 'schools':schools}
    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'peer_reply/ask.html', context_dict)


def add_course(request, university_name_slug):
    try:
        uni = University.objects.get(slug=university_name_slug)
    except University.DoesNotExist:
        uni = None

    # A HTTP POST?
    if request.method == 'POST':
        form = CourseForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            if uni:
                course = form.save(commit=False)
                course.university = uni
                course.save()
                # probably better to use a redirect here.
                return render(request, 'peer_reply/index.html')
        else:
            print form.errors
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)

    else:
        # If the request was not a POST, display the form to enter details.
        form = CourseForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'peer_reply/index.html', {'form': form})


def search(request, course_name_slug):
    """generate  search  suggestions"""
    # get 
    context_dict = {}
    # if request.user:
    # context_dict['user'] = request.user
    if request.method == 'GET':
        search = request.GET.get('text')
        # search = request.GET['search']
        if search:
            qset = Q()
            for term in search.split():
                qset |= Q(title__contains=term)

            # matching_results = YourModel.objects.filter(qset)
            context_dict['questions'] = Question.objects.filter(qset).order_by('-views')[:20]
        return render(request, 'peer_reply/course.html', context_dict)
    else:
        course = Course.objects.get(slug=course_name_slug)
        context_dict['questions'] = Question.objects.all().filter(course=course).order_by('-views')[:20]
        return render(request, 'peer_reply/course.html', context_dict)


def get_levels(request):
    if request.method == 'GET':

        school_id = request.GET['school_id']
        cur_school = School.objects.get(id=int(school_id))

        if cur_school:
            levels = Level.objects.all().filter(school=cur_school)
            level_list = []
            for level in levels:
                level_list.append('<option value="' + str(level.id) + '">' + level.name + '</option>')


    return HttpResponse(level_list)


def get_courses(request):
    if request.method == 'GET':

        level_id = request.GET['level_id']
        cur_level = School.objects.get(id=int(level_id))

        if cur_level:
            courses = Course.objects.all().filter(level=cur_level)
            course_list = []
            for course in courses:
                course_list.append('<option value="' + str(course.id) + '">' + course.name + '</option>')


    return HttpResponse(course_list)
        #  search  for  pattern  from  list
        # html = render_to_string( 'index.html', { } )
        # res = {'html': html}
        # return HttpResponse( simplejson.dumps(res), mimetype )
        # suggestion = ""
        # suggestion_list = ["Java", "cats  hate  dogs", "raining  cats  and  dogs"]
        # for s in suggestion_list:
        #     if s.startswith(search):
        #         suggestion = s
        # # return  suggestion
        # response = HttpResponse(suggestion)
        # return response


def view_question(request, question_id, question_title_slug):
    context_dict = {}

    try:

        question = Question.objects.get(id=question_id, slug=question_title_slug)

        try:
            bestAnswer = Answer.objects.filter(question=question, is_best=True)

        except Answer.DoesNotExist:
            pass

        answers = Answer.objects.filter(question=question, is_best=False).order_by('-likes')




        # Adds our results list to the template context under name pages.
        context_dict['answers'] = answers
        context_dict['best_answer'] = bestAnswer
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['question'] = question
        # Pass the slug
        context_dict['question_slug'] = question_title_slug
    except Question.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass
    return render(request, 'peer_reply/view_question.html', context_dict)



def quiz(request, quiz_name_slug):
        slug=quiz_name_slug
        context_dict = {}
        points = 0
        try:            
            quiz = Quiz.objects.get(slug=quiz_name_slug)
            user = quiz.user
            likes = quiz.likes
            questions = quiz.quizquestion_set.all()
            context_dict = {'quiz':quiz,'user':user, 'likes':likes,'slug':slug, 'questions':questions}
        except:
            pass

        if request.method == 'POST':
            for question in questions:
                if question.question_string in request.POST:
                    answer = question.quizanswer_set.get(answer_string=request.POST[question.question_string])
                    if answer.correct_answer:
                        points=points+1
            context_dict['points']=points
            return render(request,'peer_reply/quiz_results.html', context_dict)
        
        else:
            return render(request,'peer_reply/quiz.html',context_dict)
        
        return render(request,'peer_reply/quiz.html',context_dict)
