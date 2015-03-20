from django.shortcuts import render
from django.http import HttpResponse
from django.forms.formsets import formset_factory
from peer_reply.models import University, School, Level, UserProfile, Question, Answer, Quiz, Course, LevelName, \
    QuizAnswer, QuizQuestion
from peer_reply.forms import CourseForm, QuestionForm, QuizForm, QuizQuestionForm, QuizAnswerForm
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.db.models import Q
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.templatetags.static import static

# @ensure_csrf_cookie
def index(request):
    # Query the database for the universities ordered by name

    universities = University.objects.order_by('-name')[:1]
    university = University.objects.get(slug='university-of-glasgow')
    school_list = School.objects.all().filter(university=university).order_by('-name')
    # levels = Level.objects.all()

    context_dict = {'schools': school_list, 'universities': universities}
    levels = LevelName.objects.all().order_by('name')
    context_dict['levels'] = levels

    if request.user.is_authenticated():
        user_profile = request.user.profile
        relevant_questions = []
        # print user_profile.courses
        for course in user_profile.courses.all():  # for all courses in the user
            # append relevant questions in order
            relevant_questions += Question.objects.all().filter(course=course).order_by('-views')[:8]
        # add the list to ontext_dict
        context_dict['relevant_questions'] = relevant_questions
        context_dict['levels'] = levels
        return render(request, 'peer_reply/index.html', context_dict)
    else:
        print "YAY" * 20
        # if not logged in then get most recent questions
        recent_questions = Question.objects.all().order_by('-created')[:8]
        print recent_questions

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
    levels = LevelName.objects.all().order_by('name')

    context_dict['levels'] = levels
    context_dict['user_profile'] = userprofile
    return {context_dict}


def course(request, course_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}
    levels = LevelName.objects.all().order_by('name')
    context_dict['levels'] = levels
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

    university = University.objects.get(slug='university-of-glasgow')
    schools = School.objects.all().filter(university=university).order_by('name')
    context_dict['schools'] = schools
    # A HTTP POST?
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        course = request.POST['course']
        # Have we been provided with a valid form?

        if form.is_valid():
            if course:
                question = form.save(commit=False)
                question.course = Course.objects.get(id=course)
                question.user = request.user
                question.save()
                # probably better to use a redirect here.
                return HttpResponseRedirect('/peer_reply/')
        else:

            context_dict['error'] = 'error'
            context_dict['form'] = form
            return render(request, 'peer_reply/ask.html', context_dict)

    else:

        # If the request was not a POST, display the form to enter details.
        form = QuestionForm()
        context_dict = {'form': form, 'schools': schools}
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

    levels = LevelName.objects.all().order_by('name')
    context_dict['levels'] = levels
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


def get_questions(request):
    if request.method == 'GET':
        questions = None
        rank = request.GET['page_rank']
        if rank == 'recent':
            questions = Question.objects.all().order_by('-created')[:20]
        elif rank == 'hot':
            questions = Question.objects.all().order_by('views')[:20]
        # cu = School.objects.get(id=int(level_id))
        question_list = []
        if questions:

            for question in questions:
                question_list.append(
                    '<a><div class="question_link"><div class="question_link_title">' + question.title + '</div><img width="30" height="30" src="' + static('images/default-user-icon-profile.png') +'" class="question_link_pic"/><div class="question_link_username">' + question.user.username + '</div><div class="question_link_views">Views:' + str(
                        question.views) + '</div><div class="question_link_posted">Posted:' + question.created.strftime(
                        '%b,%d,%Y,%H:%M %P') + '</div></div></a>')

        return HttpResponse(question_list)
        # search  for  pattern  from  list
        # html = render_to_string( 'index.html', { } )
        # res = {'html': html}
        # return HttpResponse( simplejson.dumps(res), mimetype )
        # suggestion = ""
        # suggestion_list = ["Java", "cats  hate  dogs", "raining  cats  and  dogs"]
        # for s in suggestion_list:
        # if s.startswith(search):
        # suggestion = s
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

        levels = LevelName.objects.all().order_by('name')
        context_dict['levels'] = levels

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


@login_required
def profile(request):
    # user = User.objects.get(username=username)
    # boolean for checking if the requested profile is the logged in users.

    profile = request.user.profile
    try:
        # profile = UserProfile.objects.get(user=user)
        courses = profile.courses.all()
    except UserProfile.DoesNotExist:
        profile = None
        courses = None

    context_dict = {'profile': profile, 'courses': courses}
    university = University.objects.get(slug='university-of-glasgow')
    schools = School.objects.all().filter(university=university).order_by('name')
    context_dict['schools'] = schools
    return render(request, 'peer_reply/profile.html', context_dict)


@login_required
def edit_profile(request):
    # create a profile if it does not exist.
    user_profile = UserProfile.objects.get(user=request.user)

    # save the details
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            # re-assign the values if they exist.
            user_profile.website = request.POST['website']
            if 'picture' in request.FILES:
                user_profile.picture = request.FILES['picture']
            if 'course' in request:
                user_profile.courses += course
            user_profile.save()
            user.save()
            url = "/peer_reply/profile/" + request.user.username + "/"
            return redirect(url)

        else:
            print form.errors
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'peer_reply/edit_profile.html', {'form': form, 'user_profile': user_profile})