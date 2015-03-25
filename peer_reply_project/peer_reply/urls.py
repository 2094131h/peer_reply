from django.conf.urls import patterns, url
from peer_reply import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^/left_block/$', views.left_block, name='left_block'),
    url(r'^course/(?P<course_name_slug>[\w\-]+)/$', views.course, name='course'),
    url(r'^school/(?P<school_name_slug>[\w\-]+)/$', views.school, name='school'),

    # url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^search/$', views.search, name='search'),

    url(r'^uni/(?P<university_name_slug>[\w\-]+)/add_course/$', views.add_course, name='add_course'),
    url(r'^ask/$', views.add_question, name='add_question'),
    url(r'^get_levels/$', views.get_levels, name='get_levels'),
    url(r'^get_courses/$', views.get_courses, name='get_courses'), 
    url(r'^get_course_questions/$', views.get_course_questions, name='get_course_questions'),
    url(r'^get_search_questions/$', views.get_search_questions, name='get_search_questions'),
    url(r'^get_index_questions/$', views.get_index_questions, name='get_index_questions'),
    url(r'^ask/(?P<course_name_slug>[\w\-]+)/$', views.add_question, name='add_question'),
    url(r'^quiz/(?P<quiz_name_slug>[\w\-]+)/$', views.quiz, name='quiz'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^add_profile/$', views.add_profile, name='add_profile'),
    url(r'^add_quiz/(?P<course_name_slug>[\w\-]+)$', views.add_quiz, name='add_quiz'),
    url(r'^edit_quiz/(?P<quiz_name_slug>[\w\-]+)$', views.edit_quiz, name='edit_quiz'),
    url(r'^add_quiz_question/(?P<quiz_name_slug>[\w\-]+)$', views.add_quiz_question, name='add_quiz_question'),
    url(r'^quiz/(?P<quiz_name_slug>[\w\-]+)/quiz_results/', views.quiz, name='quiz_results'),
    url(r'^users/', views.user_profiles, name='user_profiles'),
    url(r'^rate_answer/$', views.rate_answer, name='rate_answer'),
    url(r'^flag_answer/$', views.flag_answer, name='flag_answer'),
    url(r'^mark_as_best_answer/$', views.mark_as_best_answer, name='mark_as_best_answer'),
    url(r'^question/(?P<question_id>[\w\-]+)/(?P<question_title_slug>[\w\-]+)/$', views.view_question, name='view_question'),
    url(r'^like_quiz/$', views.like_quiz, name='like_quiz'),


)


