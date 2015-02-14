from django.conf.urls import patterns, url
from peer_reply import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^course/(?P<course_name_slug>[\w\-]+)/$', views.course, name='course'),
    url(r'^uni/(?P<university_name_slug>[\w\-]+)/add_course/$', views.add_course, name='add_course'),)

