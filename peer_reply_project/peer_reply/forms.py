from django import forms
from peer_reply.models import Course, UserProfile, Question
from django.contrib.auth.models import User


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

    class Meta:
        model = UserProfile
        fields = ('website', 'picture')


