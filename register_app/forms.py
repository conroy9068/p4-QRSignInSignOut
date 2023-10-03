from django import forms
from .models import Location, Project, UserProfile
from django.contrib.auth.models import User
from django import forms


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['company_name', 'date_of_birth', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords must match.')

class SelectProjectForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all())

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_code', 'project_status', 'project_url', 'site_manager_name', 'site_manager_email', 'project_manager_name', 'project_manager_email']

LocationFormSet = forms.inlineformset_factory(
    Project, Location,
    fields=('name', 'address', 'description'),
    extra=1,
    can_delete=True
)


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
