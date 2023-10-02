from django import forms
from .models import Location, Project
from django.contrib.auth.models import User
from django import forms

class SelectProjectForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all())

class LocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', None)
        super(LocationForm, self).__init__(*args, **kwargs)
        if project_id:
            self.fields['name'].queryset = Location.objects.filter(project_id=project_id)

    class Meta:
        model = Location
        fields = ['name', 'address', 'description']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class SelectLocationSignInOut(forms.Form):
    location = forms.ModelChoiceField(
        queryset=Location.objects.filter(is_active=True), 
        label="Select Project",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
