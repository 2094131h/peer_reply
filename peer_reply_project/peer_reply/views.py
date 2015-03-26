from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import password_change
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from peer_reply.models import University, School, Level, UserProfile, Question, Answer, Quiz, Course, LevelName, QuizQuestion
from peer_reply.forms import CourseForm, QuestionForm, QuizForm, QuizQuestionForm, QuizAnswerForm, UserProfileForm, \
    AnswerForm
from django.templatetags.static import static
# from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.db.models import Q
import datetime
import json
from django.templatetags.static import static
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
import operator


# renders the home page and displays questions ordered by date/time created
def index(request):

    context_dict = get_left_block_content()



    if request.user.is_authenticated():
        user_profile = request.user.profile
        relevant_questions = []
        # print user_profile.courses
        for course in user_profile.courses.all():  # for all courses in the user

            # append relevant questions in order
            relevant_questions += Question.objects.all().filter(course=course).order_by('-created')
        relevant_questions = sorted(relevant_questions, key=operator.attrgetter('created'), reverse=True)


    else:

        # if not logged in then get most recent questions

        relevant_questions = Question.objects.all().order_by('-created')

    paginator = Paginator(relevant_questions, 10)
    questions = paginator.page(1)
    context_dict['questions'] = questions
    context_dict['top_quizzes'] = Quiz.objects.all().order_by('-likes')[:5]
    context_dict['paginator'] = paginator
    return render(request, 'peer_reply/index.html', context_dict)

#returns the objects needed to fill the left navigation bar
def get_left_block_content():

    context_dict ={}

    universities = University.objects.order_by('-name')[:1]
    university = University.objects.get(slug='university-of-glasgow')
    school_list = School.objects.all().filter(university=university).order_by('-name')
    levels = LevelName.objects.all().order_by('name')
    context_dict['levels'] = levels
    context_dict = {'schools': school_list, 'universities': universities, 'levels': levels}
    return context_dict

# Used to return questions for the index page when the 'Hot' or 'Recent' tabs are clicked
# Aslo returns a new page of questions for when the load more button is clicked
def get_index_questions(request):
    if request.method == 'GET':
        questions = []
        rank = request.GET['page_rank']

        if request.user.is_authenticated():
            user_profile = request.user.profile

            if rank == "Recent":
                for course in user_profile.courses.all():  # for all courses in the user

                    # append relevant questions in order
                    questions += Question.objects.filter(course=course)
                questions = sorted(questions, key=operator.attrgetter('created'), reverse=True)
            elif rank == "Hot":
                for course in user_profile.courses.all():  # for all courses in the user
                    pass
                    # append relevant questions in order
                    questions += Question.objects.filter(course=course)
                questions = sorted(questions, key=operator.attrgetter('views'), reverse=True)
        else:

            if rank == 'Recent':
                questions = Question.objects.order_by('-created')
            elif rank == 'Hot':
                questions = Question.objects.order_by('-views')

        paginator = Paginator(questions, 10)
        try:
            page = request.GET['page']
            questions = paginator.page(int(page))

        except:
            questions = paginator.page(1)

        question_list   = get_question_list(questions, paginator)
        return HttpResponse(question_list)

# returns questions in html format to add or append to current list
def get_question_list(questions, paginator):
        question_list = []
        if questions:

            for question in questions:

                question_list.append(
                    '<a href="' + '/peer_reply/question/' + str(question.id) +'/' + question.slug +'"><div class="question_link"><div class="question_link_title">' + question.title + '</div><div class="question_link_text">' + question.body[:200] + '</div></a></a><a href="/peer_reply/profile/' + question.user.username + '"><img width="30" height="30" src="' + static(
                        question.user.profile.picture.url) + '" class="question_link_pic"/></a><div class="question_link_username">' + question.user.username + '</div><div class="question_link_views">Views:' + str(
                        question.views) + '</div><div class="question_link_answers">Answers:' + str(
                        question.answer_set.count()) + '</div><div class="question_link_posted">Posted:' + question.created.strftime(
                        '%b,%d,%Y,%I:%M %P') + '</div><div class="rep-pic"><img width="60" height="60" class="square-rep-pic" src="' + static(question.user.profile.rep_image.url) + '"/></div></div>')
        if paginator:
            question_list.append('<input type="hidden" value="' + str(paginator.count) + '" id="course_paginator-count"/>')

        return question_list


# def left_block(request):
#     context_dict = {}
#     if request.user.is_authenticated():

#         user_profile = request.user.profile
#         # user = User.objects.get(username=user.username)

#         # userprofile = UserProfile.objects.all().filter(user=user)
#         context_dict['user_profile'] = user_profile
#     else:
#         universities = University.objects.order_by('-name')[:1]
#         university = University.objects.get(slug='university-of-glasgow')
#         school_list = School.objects.all().filter(university=university).order_by('-name')
#         context_dict['schools'] = School.objects.all().filter(university=university).order_by('-name')
#     # Render the response and send it back!
#     return render(request, 'peer_reply/left_block.html', context_dict)

# render the course pase which displays questions in the specified course
def course(request, course_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        context_dict = get_left_block_content()
        cur_course = Course.objects.get(slug=course_name_slug)
        context_dict['course'] = cur_course
        context_dict['questions'] = Question.objects.all().filter(course=cur_course).order_by('-views')[:10]
        context_dict['top_quizzes'] = Quiz.objects.filter(course=cur_course).order_by('-likes')[:5]
    except Course.DoesNotExist:

        pass

    # Go render the response and return it to the client.
    return render(request, 'peer_reply/course.html', context_dict)

# render the course pase which displays questions in the specified course
def quizzes(request, course_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        context_dict = get_left_block_content()
        cur_course = Course.objects.get(slug=course_name_slug)
        context_dict['course'] = cur_course
        context_dict['quizzes'] = Quiz.objects.all().filter(course=cur_course).order_by('-likes')[:10]

    except Course.DoesNotExist:

        pass

    # Go render the response and return it to the client.
    return render(request, 'peer_reply/quizzes.html', context_dict)

# returns quizzes in html format to add or append to current list in the quizzes page
# quizzes will be orderd by date/time or views depending on Ajax call params
def get_quizzes(request):
    if request.method == 'GET':
        quizzes = None
        rank = request.GET['page_rank']
        course_slug = request.GET['course_slug']
        qcourse = Course.objects.get(slug=course_slug)
        if rank == 'Recent':
            quizzes = Quiz.objects.filter(course=qcourse).order_by('-created')
        elif rank == 'Hot':
            quizzes = Quiz.objects.filter(course=qcourse).order_by('-likes')

        paginator = Paginator(quizzes, 10)
        try:
            page = request.GET['page']
            quizzes = paginator.page(int(page))
        except:
            pass
        quizzes = paginator.page(1)
        quiz_list = []
        if quizzes:

            for quiz in quizzes:

                quiz_list.append(
                    '<a href="' + '/peer_reply/quiz/' + quiz.slug +'"><div class="question_link"><div class="question_link_title">' + quiz.name + '</div></a></a><a href="/peer_reply/profile/' + quiz.user.username + '"><img width="30" height="30" src="' + static(
                        quiz.user.profile.picture.url) + '" alt="user avatar" class="question_link_pic"/></a><div class="question_link_username">' + quiz.user.username + '</div><div class="question_link_views">Views:' + str(
                        quiz.likes) + '</div><div class="question_link_posted">Posted:' + quiz.created.strftime(
                        '%b,%d,%Y,%I:%M %P') + '</div><div class="rep-pic"><img width="60" height="60" class="square-rep-pic" src="' + static(quiz.user.profile.rep_image.url) + '" alt="reputation award"/></div></div>')
            if paginator:
                quiz_list.append('<input type="hidden" value="' + str(paginator.count) + '" id="quiz_paginator-count"/>')

        return HttpResponse(quiz_list)

# render the page for postiing questions
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


# renders the page whick displays search results when user enters a search in navbar
def search(request):
    context_dict = get_left_block_content()

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

# return levels in a course specified in Ajax request
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

# return courses in a course specified in Ajax request
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

# returns questions in html format to add or append to current list in the course page
# questions qill be orderd by date/time or views depending on Ajax call params
def get_course_questions(request):
    if request.method == 'GET':
        questions = None
        rank = request.GET['page_rank']
        course_slug = request.GET['course_slug']
        course = Course.objects.get(slug=course_slug)
        if rank == 'Recent':
            questions = Question.objects.filter(course=course).order_by('-created')
        elif rank == 'Hot':
            questions = Question.objects.filter(course=course).order_by('-views')
        paginator = Paginator(questions, 10)
        try:
            page = request.GET['page']
            questions = paginator.page(int(page))

        except:
            pass

        questions = paginator.page(1)

        question_list   = get_question_list(questions, paginator)
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

        if rank == 'Recent':
            questions = Question.objects.filter(qset).order_by('-created')
        elif rank == 'Hot':
            questions = Question.objects.filter(qset).order_by('-views')

        # create paginator to return questions in pages of size 10
        paginator = Paginator(questions, 10)
        try:
            page = request.GET['page']
            questions = paginator.page(int(page))

        except:
            questions = paginator.page(1)
        question_list = get_question_list(questions, paginator)
        return HttpResponse(question_list)

# renders the page for viewing a particular question and any answers which have been added to it
def view_question(request, question_id, question_title_slug):
    context_dict = {}
    context_dict = get_left_block_content()
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
                bestAnswerUser = bestAnswer.user
                bestAnswerUserProfile = UserProfile.objects.get(user=bestAnswerUser)
                context_dict['best_answer'] = bestAnswer
                context_dict['best_answer_user'] = bestAnswerUserProfile
            except Answer.DoesNotExist:
                pass

            answers = Answer.objects.filter(question=question, is_best=False, flags__lt=4).order_by('-likes')
            userask = Question.objects.get(id=question_id).user
            useraskprofile = UserProfile.objects.get(user=userask)

            # Added to load courses in left navbar

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

                if (datetime.now() - last_visit_time).seconds > 5:
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


# adds likes to anwers specified in Ajax request
def rate_answer(request):
    answer_id = None
    if request.method == 'GET':
        answer_id = request.GET['answer_id']

    if answer_id:
        answer = Answer.objects.get(id=int(answer_id))
        if answer:
            rating = answer.likes + 1
            answer.likes = rating
            answer.save()

    return HttpResponse()

# adda likes to a quiz
def like_quiz(request):
    quiz_id = None
    if request.method == 'GET':
        quiz_id = request.GET['quiz_id']

    if quiz_id:
        quiz = Quiz.objects.get(id=int(quiz_id))
        if quiz:
            rating = quiz.likes + 1
            quiz.likes = rating
            quiz.save()

    return HttpResponse()

# adds flags to anwers specified in Ajax request
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

# marks an answer to a particular question as the best answer.
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

# renders the page for viewing a particular quiz
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
        try:
            quiz = Quiz.objects.get(slug=quiz_name_slug)
        except Quiz.DoesNotExist:
            pass
        context_dict = get_left_block_content()
        context_dict['points'] = points
        context_dict['quiz'] = quiz

        return render(request, 'peer_reply/quiz_results.html', context_dict)

    else:
        return render(request, 'peer_reply/quiz.html', context_dict)

    return render(request, 'peer_reply/quiz.html', context_dict)

# render the page for adding a quiz to a specified course
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
                return redirect('/peer_reply/edit_quiz/' + quiz.slug)
        else:
            print quizForm.errors  # Can I handle errors in a better way?
    else:
        quizForm = QuizForm()
    # I will have to pass quiz-name-slug also since I use it for adding quiz question link.
    context_dict['form'] = quizForm

    return render(request, 'peer_reply/add_quiz.html', context_dict)


@login_required
def edit_quiz(request, quiz_name_slug):
    context_dict = {}
    quiz = Quiz.objects.get(slug=quiz_name_slug)

    if quiz:
        context_dict['quiz'] = quiz
    else:
        pass

    quiz_questions = QuizQuestion.objects.filter(quiz=quiz)
    if quiz_questions:
        context_dict['quiz_questions'] = quiz_questions
    else:
        pass

    return render(request, 'peer_reply/edit_quiz.html', context_dict)


# renders the page for adding questions to a particular quiz
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
                context_dict['quiz_course_slug'] = quiz.course.slug

                return redirect('/peer_reply/edit_quiz/' + quiz_name_slug)

                #return render(request, 'peer_reply/add_quiz_question.html', context_dict)  #Redirect to same, empty page
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

# renders the page for viewing a particular users profile
def profile(request, username):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        user_profile = UserProfile.objects.get(user=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            # for users to add/remove courses to their profiles
            if 'rem-course-input' in request.POST:
                # for users to add/remove courses to their profiles
                if request.POST['rem-course-input'] != '':
                    rem_course_list = request.POST['rem-course-input'].replace('\r', '').split(",")
                    for course in rem_course_list:
                        course = Course.objects.all().filter(name=course).first()
                        user_profile.courses.remove(course)
                if request.POST['select-course-input'] != '':
                    # last item in list is empty, so remove that from list.
                    add_course_list = request.POST['select-course-input'].replace('\r', '').split(",")[:-1]
                    for course in add_course_list:
                        course = Course.objects.all().filter(name=course).first()
                        user_profile.courses.add(course)
                        user_profile.save()
            user_profile.save()
            user.save()

    university = University.objects.get(slug='university-of-glasgow')
    schools = School.objects.all().filter(university=university).order_by('name')
    user = User.objects.get(username=username)
    # boolean for checking if the requested profile is the logged in users.
    user_profile = (request.user==user)
    try:
        profile = UserProfile.objects.get(user=user)
        courses = profile.courses.all()
    except UserProfile.DoesNotExist:
        profile = None
        courses = None

    context_dict = {'user':user,'profile':profile,'user_profile':user_profile,'courses':courses,'schools': schools}

    my_question = Question.objects.filter(user=user)
    my_quiz = Quiz.objects.filter(user=user)
    context_dict['my_question'] = my_question
    context_dict['my_quiz'] = my_quiz

    return render(request, 'peer_reply/profile.html',context_dict)

# render the page for users to edit their profile
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

            if request.POST['rem-pic'] == "true":
                user_profile.picture = None

            user_profile.save()
            user.save()
            url = "/peer_reply/profile/"+request.user.username+"/"
            return redirect(url)

        else:
            print form.errors
    else:
        form = UserProfileForm(instance=request.user)
    return render(request,'peer_reply/edit_profile.html',{'form':form,'user_profile':user_profile})

# render page for users to add their profile details
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
            url = "/peer_reply/profile/"+request.user.username+"/"
            return redirect(url)
        else:
            print form.errors
    else:
        form = UserProfileForm(instance=request.user)
    return render(request,'peer_reply/edit_profile.html',{'form':form})

# renders page for viewing the top 20 registered users
def user_profiles(request):
    context_dict = {}
    context_dict['users'] = UserProfile.objects.order_by('-no_quiz_likes', '-no_best_answers')[:20]
    return render(request, 'peer_reply/users.html', context_dict)
