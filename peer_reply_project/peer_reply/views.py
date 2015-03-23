from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import password_change
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from peer_reply.models import University, School, Level, UserProfile, Question, Answer, Quiz, Course, LevelName, \
    QuizAnswer, QuizQuestion
from peer_reply.forms import CourseForm, QuestionForm, QuizForm, QuizQuestionForm, QuizAnswerForm, UserProfileForm, \
    AnswerForm
from django.templatetags.static import static
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.db.models import Q
import datetime
import json
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, HttpResponse
from django.templatetags.static import static
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import datetime
import operator



# @ensure_csrf_cookie
def index(request):
    context_dict = {}
    universities = University.objects.order_by('-name')[:1]
    university = University.objects.get(slug='university-of-glasgow')
    school_list = School.objects.all().filter(university=university).order_by('-name')

    context_dict = {'schools': school_list, 'universities': universities}
    levels = LevelName.objects.all().order_by('name')
    context_dict['levels'] = levels

    if request.user.is_authenticated():
        user_profile = request.user.profile
        relevant_questions = []
        # print user_profile.courses
        for course in user_profile.courses.all():  # for all courses in the user

            # append relevant questions in order
            relevant_questions += Question.objects.all().filter(course=course).order_by('-created')
        relevant_questions = sorted(relevant_questions, key=operator.attrgetter('created'), reverse=True)
        context_dict['levels'] = levels

    else:

        # if not logged in then get most recent questions

        relevant_questions = Question.objects.all().order_by('-created')

    paginator = Paginator(relevant_questions, 10)
    questions = paginator.page(1)

    context_dict['questions'] = questions
    context_dict['top_quizzes'] = Quiz.objects.all().order_by('likes')[:5]
    context_dict['paginator'] = paginator
    return render(request, 'peer_reply/index.html', context_dict)


def get_index_questions(request):
    if request.method == 'GET':
        questions = []
        rank = request.GET['page_rank']

        if request.user.is_authenticated():
            user_profile = request.user.profile

            if rank == "recent":
                for course in user_profile.courses.all():  # for all courses in the user

                    # append relevant questions in order
                    questions += Question.objects.filter(course=course)
                questions = sorted(questions, key=operator.attrgetter('created'), reverse=True)
            elif rank == "hot":
                for course in user_profile.courses.all():  # for all courses in the user
                    pass
                    # append relevant questions in order
                    questions += Question.objects.filter(course=course)
                questions = sorted(questions, key=operator.attrgetter('views'), reverse=True)
        else:

            if rank == 'recent':
                questions = Question.objects.order_by('-created')
            elif rank == 'hot':
                questions = Question.objects.order_by('-views')

        paginator = Paginator(questions, 10)
        try:
            page = request.GET['page']
            questions = paginator.page(int(page))

        except:
            questions = paginator.page(1)

        question_list = []
        if questions:

            for question in questions:


                question_list.append(
                    '<a href="' + '/peer_reply/question/' + str(question.id) +'/' + question.slug +'"><div class="question_link"><div class="question_link_title">' + question.title + '</div><div class="question_link_text">' + question.body[:200] + '</div></a></a><a href="/peer_reply/profile/' + question.user.username + '"><img width="30" height="30" src="' + static(
                        question.user.profile.picture.url) + '" class="question_link_pic"/></a><div class="question_link_username">' + question.user.username + '</div><div class="question_link_views">Views:' + str(
                        question.views) + '</div><div class="question_link_answers">Answers:' + str(
                        question.answer_set.count()) + '</div><div class="question_link_posted">Posted:' + question.created.strftime(
                        '%b,%d,%Y,%I:%M %P') + '</div></div>')
        question_list.append('<input type="hidden" value="' + str(paginator.count) + '" id="course_paginator-count"/>')

        return HttpResponse(question_list)


def left_block(request):
    context_dict = {}
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
    context_dict = {}
    user = request.user
    userprofile = UserProfile.objects.get(user=user)
    levels = LevelName.objects.all().order_by('name')

    context_dict['levels'] = levels
    context_dict['user_profile'] = userprofile
    return {context_dict}


def course(request, course_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        universities = University.objects.order_by('-name')[:1]
        university = University.objects.get(slug='university-of-glasgow')
        school_list = School.objects.all().filter(university=university).order_by('-name')
        context_dict['schools'] = school_list
        context_dict['universities'] = universities
        levels = LevelName.objects.all().order_by('name')
        context_dict['levels'] = levels

        cur_course = Course.objects.get(slug=course_name_slug)
        context_dict['course'] = cur_course
        context_dict['universities'] = University.objects.order_by('-name')[:1]
        context_dict['questions'] = Question.objects.all().filter(course=cur_course).order_by('-views')[:10]
        context_dict['top_quizzes'] = Quiz.objects.filter(course=cur_course).order_by('likes')[:5]
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


@login_required
def add_question(request):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    university = University.objects.get(slug='university-of-glasgow')
    schools = School.objects.all().filter(university=university).order_by('name')
    context_dict['schools'] = schools

    # A HTTP POST?
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        course_id = request.POST['course']
        # Have we been provided with a valid form?
        if form.is_valid():
            # if course:
            question = form.save(commit=False)
            question.course = Course.objects.get(id=course_id)
            question.user = request.user
            question.save()
            # probably better to use a redirect here.
            return redirect('/peer_reply/question/' + str(question.id) + '/' + str(question.slug))
        else:

            context_dict['error'] = 'error'
            context_dict['form'] = form
            return render(request, 'peer_reply/ask.html', context_dict)

    else:

        form = QuestionForm()
        context_dict['form'] = form

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


def search(request):
    universities = University.objects.order_by('-name')[:1]
    university = University.objects.get(slug='university-of-glasgow')
    school_list = School.objects.all().filter(university=university).order_by('-name')

    # levels = Level.objects.all()

    context_dict = {'schools': school_list, 'universities': universities}
    levels = LevelName.objects.all().order_by('name')
    context_dict['levels'] = levels

    # enerate  search  suggestions
    # get 

    # if request.user:
    # context_dict['user'] = request.user
    if request.method == 'GET':
        search = request.GET.get('text')
        # search = request.GET['search']
        if search:
            qset = Q()
            qqset = Q()
            for term in search.split():
                qset |= Q(title__contains=term)
                qqset |= Q(name__contains=term)
            questions = Question.objects.filter(qset).order_by('-views')
            paginator = Paginator(questions, 10)

            questions = paginator.page(1)
            context_dict['questions'] = questions

            context_dict['top_quizzes'] = Quiz.objects.filter(qqset).order_by('-likes')[:5]
            context_dict['search'] = search
        return render(request, 'peer_reply/search.html', context_dict)
        # else:
        # course = Course.objects.get(slug=course_name_slug)
        #     context_dict['questions'] = Question.objects.all().filter(course=course).order_by('-views')[:20]
        #     return render(request, 'peer_reply/course.html', context_dict)


def get_levels(request):
    if request.method == 'GET':

        school_id = request.GET['school_id']
        cur_school = School.objects.get(id=int(school_id))

        if cur_school:
            levels = Level.objects.all().filter(school=cur_school)
            level_list = []
            for level in levels:
                level_list.append('<option value="' + str(level.id) + '">' + level.name.name + '</option>')

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


def get_course_questions(request):
    if request.method == 'GET':
        questions = None
        rank = request.GET['page_rank']
        if rank == 'recent':
            questions = Question.objects.all().order_by('-created')
        elif rank == 'hot':
            questions = Question.objects.all().order_by('-views')

        try:
            paginator = Paginator(questions, 10)
            page = request.GET['page']
            questions = paginator.page(int(page))
        except:
            pass

        # cu = School.objects.get(id=int(level_id))
        question_list = []
        if questions:

            for question in questions:
                question_list.append(
                    '<a href="' + '/peer_reply/question/' + str(question.id) +'/' + question.slug +'"><div class="question_link"><div class="question_link_title">' + question.title + '</div><div class="question_link_text">' + question.body[:200] + '</div></a></a><a href="/peer_reply/profile/' + question.user.username + '"><img width="30" height="30" src="' + static(
                        question.user.profile.picture.url) + '" class="question_link_pic"/></a><div class="question_link_username">' + question.user.username + '</div><div class="question_link_views">Views:' + str(
                        question.views) + '</div><div class="question_link_answers">Answers:' + str(
                        question.answer_set.count()) + '</div><div class="question_link_posted">Posted:' + question.created.strftime(
                        '%b,%d,%Y,%I:%M %P') + '</div></div>')
        question_list.append('<input type="hidden" value="' + str(paginator.count) + '" id="course_paginator-count"/>')
        return HttpResponse(question_list)


# returns questions ordered by views or date created depending on which tab has been clicked
def get_search_questions(request):
    if request.method == 'GET':
        questions = None
        rank = request.GET['page_rank']
        search = request.GET['search']

        # if search exists create a query based on each word contained in the string
        if search:
            qset = Q()
            qqset = Q()
            for term in search.split():
                qset |= Q(title__contains=term)
                qqset |= Q(name__contains=term)

        if rank == 'recent':
            questions = Question.objects.filter(qset).order_by('-created')
        elif rank == 'hot':
            questions = Question.objects.filter(qset).order_by('-views')

        try:
            paginator = Paginator(questions, 5)
            page = request.GET['page']
            questions = paginator.page(int(page))

        except:
            pass

        question_list = []
        if questions:

            for question in questions:
                question_list.append(
                    '<a href="' + '/peer_reply/question/' + str(question.id) +'/' + question.slug +'"><div class="question_link"><div class="question_link_title">' + question.title + '</div><div class="question_link_text">' + question.body[:200] + '</div></a><a href="/peer_reply/profile/' + question.user.username + '"><img width="30" height="30" src="' + static(
                        question.user.profile.picture.url) + '" class="question_link_pic"/></a><div class="question_link_username">' + question.user.username + '</div><div class="question_link_views">Views:' + str(
                        question.views) + '</div><div class="question_link_answers">Answers:' + str(
                        question.answer_set.count()) + '</div><div class="question_link_posted">Posted:' + question.created.strftime(
                        '%b,%d,%Y,%I:%M %P') + '</div></div>')
            question_list.append(
                '<input type="hidden" value="' + str(paginator.count) + '" id="search-paginator-count"/>')
        return HttpResponse(question_list)


def view_question(request, question_id, question_title_slug):
    context_dict = {}

    if request.method == 'POST':
        form = AnswerForm(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = Question.objects.get(id=question_id, slug=question_title_slug)
            answer.likes = 0
            answer.is_best = False
            answer.user = request.user
            answer.save()
        else:
            print form.errors
        if 'next' in request.GET:
            return redirect(request.GET['next'])

    if request.method == 'GET':

        try:
            question = Question.objects.get(id=question_id, slug=question_title_slug)

            try:
                bestAnswer = Answer.objects.get(question=question, is_best=True, flags__lt=4)
                bestAnswerUser = Answer.objects.get(question=question, is_best=True).user
                bestAnswerUserProfile = UserProfile.objects.get(user=bestAnswerUser)
                context_dict['best_answer'] = bestAnswer
                context_dict['best_answer_user'] = bestAnswerUserProfile
            except Answer.DoesNotExist:
                pass

            answers = Answer.objects.filter(question=question, is_best=False, flags__lt=4).order_by('-likes')
            userask = Question.objects.get(id=question_id).user
            useraskprofile = UserProfile.objects.get(user=userask)

            # Added to load courses in left navbar
            universities = University.objects.order_by('-name')[:1]
            university = University.objects.get(slug='university-of-glasgow')
            school_list = School.objects.all().filter(university=university).order_by('-name')
            context_dict['schools'] = school_list
            context_dict['universities'] = universities
            levels = LevelName.objects.all().order_by('name')
            context_dict['levels'] = levels
            context_dict['top_quizzes'] = Quiz.objects.filter(course=question.course).order_by('-likes')[:5]
            context_dict['answers'] = answers
            context_dict['userask'] = userask
            context_dict['useraskprofile'] = useraskprofile
            context_dict['question'] = question
            context_dict['question_slug'] = question_title_slug
            form = AnswerForm()
            context_dict['form'] = form

            no_of_answers = Answer.objects.filter(question=question, flags__lt=4).count()
            context_dict['no_of_answers'] = no_of_answers

            response = render(request, 'peer_reply/view_question.html', context_dict)

            # Increments page views but only if the user hasn't viewed it in a day.
            reset_last_visit_time = False
            if 'last_visit' in request.COOKIES:
                last_visit = request.COOKIES['last_visit']
                last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

                if (datetime.now() - last_visit_time).days > 0:
                    question.views = question.views + 1
                    question.save()
                    reset_last_visit_time = True
            else:
                reset_last_visit_time = True

            if reset_last_visit_time:
                response.set_cookie('last_visit', datetime.now())

        except Question.DoesNotExist:
            pass

        return response


# <<<<<<< HEAD
# levels = LevelName.objects.all().order_by('name')
#         context_dict['levels'] = levels
# =======

def rate_answer(request):
    answer_id = None
    if request.method == 'GET':
        answer_id = request.GET['answer_id']
    # >>>>>>> 66ca913677134329e1642a7026f744cc9375383a

    if answer_id:
        answer = Answer.objects.get(id=int(answer_id))
        if answer:
            rating = answer.likes + 1
            answer.likes = rating
            answer.save()

    return HttpResponse()


def flag_answer(request):
    answer_id = None
    if request.method == 'GET':
        answer_id = request.GET['answer_id']

    if answer_id:
        answer = Answer.objects.get(id=int(answer_id))
        if answer:
            flag = answer.flags + 1
            answer.flags = flag
            answer.save()
    return HttpResponse()


def mark_as_best_answer(request):
    answer_id = None
    if request.method == 'GET':
        answer_id = request.GET['answer_id']

    if answer_id:
        answer = Answer.objects.get(id=int(answer_id))
        if answer:
            answer.is_best = True
            answer.save()
        user = UserProfile.objects.get(user=answer.user)
        if user:
            best_answers = user.no_best_answers + 1
            user.no_best_answers = best_answers
            user.save()

    return HttpResponse()


def quiz(request, quiz_name_slug):
    slug = quiz_name_slug
    context_dict = {}
    points = 0
    try:
        quiz = Quiz.objects.get(slug=quiz_name_slug)
        user = quiz.user
        likes = quiz.likes
        questions = quiz.quizquestion_set.all()
        context_dict = {'quiz': quiz, 'user': user, 'likes': likes, 'slug': slug, 'questions': questions}

    except:
        pass

    if request.method == 'POST':
        for question in questions:
            if question.question_string in request.POST:
                answer = question.quizanswer_set.get(answer_string=request.POST[question.question_string])
                if answer.correct_answer:
                    points = points + 1
        context_dict['points'] = points
        return render(request, 'peer_reply/quiz_results.html', context_dict)

    else:
        return render(request, 'peer_reply/quiz.html', context_dict)

    return render(request, 'peer_reply/quiz.html', context_dict)


@login_required
def add_quiz(request, course_name_slug):  # Any other parameters required?

    # Check if course exists
    try:
        course = Course.objects.get(slug=course_name_slug)
    except Course.DoesNotExist:
        course = None

    context_dict = {'course_name_slug': course_name_slug, 'quiz_name_slug': None}

    if request.method == 'POST':
        quizForm = QuizForm(request.POST)  # Bind data to form

        if quizForm.is_valid():
            if course:  # If there was indeed a course by that name...
                quiz = quizForm.save(commit=False)  #Saves quiz name, delay committing
                quiz.course = course
                quiz.user = request.user
                quiz.likes = 0
                quiz.save()
                quiz_name_slug = quiz.slug  ##Should now be name, slugified
                context_dict['quiz_name_slug'] = quiz_name_slug
                #return render(request, 'peer_reply/add_quiz.html', context_dict)
                return render(request, 'peer_reply/add_quiz.html', context_dict)
        else:
            print quizForm.errors  # Can I handle errors in a better way?
    else:
        quizForm = QuizForm()
    # I will have to pass quiz-name-slug also since I use it for adding quiz question link.
    context_dict['form'] = quizForm

    return render(request, 'peer_reply/add_quiz.html', context_dict)


@login_required
def add_quiz_question(request, quiz_name_slug):
    # First check if arguments exist in database
    # try:
    # course = Course.objects.get(slug=course_name_slug)
    # except Course.DoesNotExist:
    # course = None
    try:
        quiz = Quiz.objects.get(slug=quiz_name_slug)
    except Quiz.DoesNotExist:
        quiz = None

    QuizAnswerFormSet = formset_factory(QuizAnswerForm, extra=4)  #Creating four instances of form
    if request.method == 'POST':
        quizQuestionForm = QuizQuestionForm(request.POST)  #Bind data to forms
        formset = QuizAnswerFormSet(request.POST)

        if quizQuestionForm.is_valid() and formset.is_valid():
            if quiz:
                quizQuestion = quizQuestionForm.save(commit=False)  #Saving question-string, I suppose
                quizQuestion.quiz = quiz
                quizQuestion.save()

                for form in formset:
                    quizAnswer = form.save(commit=False)  #Saving answer_string and correct_answer, I suppose
                    quizAnswer.question = quizQuestion
                    quizAnswer.save()

                context_dict = {}
                # context_dict['course_name_slug'] = course_name_slug
                context_dict['quiz_name_slug'] = quiz_name_slug
                context_dict['quizQuestionForm'] = quizQuestionForm
                context_dict['formset'] = formset

                return render(request, 'peer_reply/add_quiz_question.html', context_dict)  #Redirect to same, empty page
        else:
            print quizQuestionForm.errors, formset.errors
    else:  #Instantiate forms to display
        formset = QuizAnswerFormSet()
        quizQuestionForm = QuizQuestionForm()

    context_dict = {'quizQuestionForm': quizQuestionForm}
    context_dict['formset'] = formset
    # context_dict['course_name_slug'] = course_name_slug
    context_dict['quiz_name_slug'] = quiz_name_slug

    return render(request, 'peer_reply/add_quiz_question.html', context_dict)


# pasword change functionality for the profile
@login_required
def change_password(request):
    return password_change(request, post_change_redirect='/peer_reply/profile.html')


def profile(request, username):
    user = User.objects.get(username=username)
    # boolean for checking if the requested profile is the logged in users.
    user_profile = (request.user == user)
    try:
        profile = UserProfile.objects.get(user=user)
        courses = profile.courses.all()
    except UserProfile.DoesNotExist:
        profile = None
        courses = None
    # <<<<<<< HEAD
    context_dict = {'user': user, 'profile': profile, 'user_profile': user_profile, 'courses': courses}
    university = University.objects.get(slug='university-of-glasgow')
    schools = School.objects.all().filter(university=university).order_by('name')
    context_dict['schools'] = schools

    return render(request, 'peer_reply/profile.html', context_dict)


# =======
#
#     context_dict = {'user':user,'profile':profile,'user_profile':user_profile,'courses':courses}
#     return render(request, 'peer_reply/profile.html',context_dict)
# >>>>>>> 66ca913677134329e1642a7026f744cc9375383a


@login_required
def edit_profile(request):
    # create a profile if it does not exist.
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return add_profile(request)
    # save the details
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            # re-assign the values if they exist.
            if request.POST['website'] != '':
                user_profile.website = request.POST['website']
            if request.POST['location'] != '':
                user_profile.location = request.POST['location']
            if 'picture' in request.FILES:
                user_profile.picture = request.FILES['picture']

            user_profile.save()
            user.save()
            url = "/peer_reply/profile/" + request.user.username + "/"
            return redirect(url)

        else:
            print form.errors
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'peer_reply/edit_profile.html', {'form': form, 'user_profile': user_profile})


@login_required
def add_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            # connecting the use and profile
            profile.user = request.user
            # Profile picture supplied? If so, we put it in the new UserProfile.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            url = "/peer_reply/profile/" + request.user.username + "/"
            return redirect(url)
        else:
            print form.errors
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'peer_reply/edit_profile.html', {'form': form})


def user_profiles(request):
    context_dict = {}
    context_dict['users'] = UserProfile.objects.order_by('no_quiz_likes', 'no_best_answers')
    return render(request, 'peer_reply/users.html', context_dict)
