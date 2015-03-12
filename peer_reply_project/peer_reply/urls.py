from django.conf.urls import patterns, url
from peer_reply import views
from registration.backends.simple.views import RegistrationView


# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(selfself,request, user):
        return '/peer_reply/'

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^course/(?P<course_name_slug>[\w\-]+)/$', views.course, name='course'),
    url(r'^school/(?P<school_name_slug>[\w\-]+)/$', views.school, name='school'),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^search/(?P<course_name_slug>[\w\-]+)/$', views.search, name='search'),
    url(r'^uni/(?P<university_name_slug>[\w\-]+)/add_course/$', views.add_course, name='add_course'),
    url(r'^ask/(?P<course_name_slug>[\w\-]+)/$', views.add_question, name='add_question'),)

