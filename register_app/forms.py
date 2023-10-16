from django import forms
from .models import Location, Project, UserProfile
from django.contrib.auth.models import User
from django import forms

# USER PROFILE FORMS
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


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
            
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']            


# PROJECT FORMS
class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'project_name', 'project_code', 'project_status', 'project_url',
            'site_manager_name', 'site_manager_email', 'project_manager_name', 'project_manager_email'
        ]
        widgets = {
            field: forms.TextInput(attrs={'class': 'form-control mb-2'})
            for field in ['project_name', 'project_code', 'project_url', 'site_manager_name', 'site_manager_email', 'project_manager_name', 'project_manager_email']
        }
        widgets['project_status'] = forms.Select(attrs={'class': 'form-control mb-2'})
        
LocationFormSet = forms.inlineformset_factory(
    Project, Location,
    fields=('name', 'address', 'description', 'is_active'),
    extra=1,
    can_delete=True,
    widgets={'name': forms.TextInput(attrs={'class': 'form-control'}),
             'address': forms.TextInput(attrs={'class': 'form-control'}),
             'description': forms.TextInput(attrs={'class': 'form-control'}),
             'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
             }
)
    
class ProjectSelectionForm(forms.Form):
    project = forms.ModelChoiceField(
        queryset=Project.objects.filter(project_status='Active'), 
        label="Select Project",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.none(), 
        label="Select Location",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


# LOCATION FORMS
class SelectLocationSignInOut(forms.Form):
    location = forms.ModelChoiceField(
        queryset=Location.objects.filter(is_active=True), 
        label="Select Project",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
