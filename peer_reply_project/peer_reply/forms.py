from django import forms
from peer_reply.models import Course


class CourseForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the course name.")

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Course
        fields = ('name',)


# class ModuleForm(forms.ModelForm):
#     title = forms.CharField(max_length=128, help_text="Please enter the title of the module.")
#     slug = forms.CharField(widget=forms.HiddenInput(), required=False)
#
#     class Meta:
#         # Provide an association between the ModelForm and a model
#         model = Module
#
#         # What fields do we want to include in our form?
#         # This way we don't need every field in the model present.
#         # Some fields may allow NULL values, so we may not want to include them...
#         # Here, we are hiding the foreign key.
#         # we can either exclude the category field from the form,
#         exclude = ('course',)
#         #or specify the fields to include (i.e. not include the category field)
#         #fields = ('title', 'url', 'views')
