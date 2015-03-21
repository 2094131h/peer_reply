from django import forms
from peer_reply.models import Course, UserProfile, Question, Quiz, QuizQuestion, QuizAnswer
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory


class CourseForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the course name.")

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Course
        fields = ('name',)


class QuestionForm(forms.ModelForm):

    title = forms.CharField(max_length=128, help_text="Please enter question title.")
    body = forms.Textarea()
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)


    title = forms.CharField(max_length=128, help_text="Please enter question title.", required=True)
    body = forms.Textarea()
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    course = forms.CharField(max_length=128,widget=forms.HiddenInput())
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)


    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Question
        fields = ('title', 'body', 'views')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    # An inline class to provide additional information on the form.
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
 
    username = forms.CharField(required=False)
    website = forms.URLField(help_text="Please enter your website.", required=False)
    picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)
    location = forms.CharField(help_text="Please enter your location.", required=False)

    class Meta:
        model = UserProfile
        fields = ('website', 'picture','location')


class QuizForm(forms.ModelForm):

	name = forms.CharField(max_length=60, help_text="Please enter name of quiz.")
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Quiz
		fields = ('name',)

class QuizQuestionForm(forms.ModelForm):
	question_string = forms.Textarea()

	class Meta:
		model = QuizQuestion
		fields = ('question_string',)

class QuizAnswerForm(forms.ModelForm):
	answer_string = forms.Textarea()
	correct_answer = forms.BooleanField(required=False, help_text="Correct?")

	class Meta:
		model = QuizAnswer
		fields = ('answer_string', 'correct_answer',)


