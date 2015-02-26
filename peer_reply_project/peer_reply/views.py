from django.shortcuts import render
from django.http import HttpResponse
from peer_reply.models import Course
from peer_reply.models import University, School, Level
from peer_reply.forms import CourseForm


def index(request):
    #Query the database for the universities ordered by name

    universities = University.objects.order_by('-name')[:1]
    university = University.objects.get(slug='university-of-glasgow')
    school_list = School.objects.all().filter(university=university).order_by('-name')
    levels = Level.objects.all()

    context_dict = {'schools': school_list, 'universities': universities}

    # Render the response and send it back!
    return render(request, 'peer_reply/index.html', context_dict)


def course(request, course_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:

        university = University.objects.get(slug=university_name_slug)
        course = Course.objects.get(slug=course_name_slug)

        context_dict['course_name'] = category.name
        context_dict['course_slug'] = category.slug

        modules = Module.objects.filter(course=course)

        # Adds our results list to the template context under name pages.
        context_dict['modules'] = modules

        context_dict['course'] = course
    except Course.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'peer_reply/course.html', context_dict)


def add_course( request, university_name_slug):
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
