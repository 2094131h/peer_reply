from django.contrib import admin
from peer_reply.models import University, School, Level, Course, Quiz, QuizQuestion, QuizAnswer
from peer_reply.models import Question, Answer, UserProfile
from django.contrib.auth.models import User




# Add in these classes to customized the Admin Interface
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    prepopulated_fields = {'slug':('name',)}

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username','website', 'picture', 'location', 'no_best_answers', 'no_quiz_likes', 'display_courses')
    prepopulated_fields = {'slug':('username',)}

class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'school')


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'display_levels')
    prepopulated_fields = {'slug':('name',)}


class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    prepopulated_fields = {'slug':('name',)}

class QuizAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'name', 'likes')
    prepopulated_fields = {'slug':('name',)}


class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question_string')
    prepopulated_fields = {'slug':('question_string',)}


class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer_string', 'correct_answer')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'title', 'body')
    prepopulated_fields = {'slug':('title',)}


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'body', 'likes', 'is_best')


# Update the registration to include this customised interface
admin.site.register(University, UniversityAdmin)
admin.site.register(School, SchoolAdmin)
# admin.site.register(School_Level, School_LevelAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Course, CourseAdmin,)
admin.site.register(Quiz, QuizAdmin,)
admin.site.register(QuizQuestion, QuizQuestionAdmin,)
admin.site.register(QuizAnswer, QuizAnswerAdmin,)
admin.site.register(Question, QuestionAdmin,)
admin.site.register(Answer, AnswerAdmin,)
admin.site.register(UserProfile, UserProfileAdmin,)






