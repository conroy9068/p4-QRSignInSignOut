from django import forms
from .models import Location, Project, UserProfile
from django.contrib.auth.models import User


# USER PROFILE FORMS
class UserRegistrationForm(forms.ModelForm):
    """
    A form for registering a new user. Requires the user to enter a username, email, password, and confirm password.
    """
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
    """
    A form for creating or updating a user's profile information.
    Includes fields for company name, date of birth, and phone number.
    """
    company_name = forms.CharField(required=True, widget=forms.DateInput(attrs={'class': 'form-control'}))
    class Meta:
        model = UserProfile
        fields = ['company_name', 'date_of_birth', 'phone_number' ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords must match.')


# PROJECT FORMS
class CreateProjectForm(forms.ModelForm):
    """
    A form for creating a new project.

    This form includes fields for the project name, code, status, URL, site manager name and email,
    and project manager name and email. It also includes widgets for styling the form fields.
    """
    class Meta:
        model = Project
        can_delete=True,
        fields = [
            'project_name', 'project_code', 'project_status', 'project_url',
            'site_manager_name', 'site_manager_email', 'project_manager_name', 'project_manager_email'
        ]
        widgets = {
            field: forms.TextInput(attrs={'class': 'form-control mb-2', 'id': field})
            for field in ['project_name', 'project_code', 'project_url', 'site_manager_name', 'site_manager_email', 'project_manager_name', 'project_manager_email']
        }
        widgets['project_status'] = forms.Select(attrs={'class': 'form-control mb-2', 'id': 'project_status'})
        
LocationFormSet = forms.inlineformset_factory(
    Project, Location,
    fields=('name', 'address', 'description', 'is_active'),
    extra=0,
    can_delete=True,
    widgets={'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            }
)

class CreateLocationForm(forms.ModelForm):
    """
    A form used to create a new location instance.

    This form includes fields for the location name, address, description, and whether or not the location is active.
    """
    class Meta:
        model = Location
        can_delete=True,
        fields = ['name', 'address', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        required = {
            'description': False,
        }

        
class EditLocationForm(forms.ModelForm):
    """
    A form used to edit a location instance.

    This form includes fields for the location name, address, description, and whether or not the location is active.
        
    """
    class Meta:
        model = Location
        fields = ['name', 'address', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    
class ProjectSelectionForm(forms.Form):
    """
    A form used to select a project and location.

    """
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
    """
    A form for selecting a location for sign in/out.
    """
    location = forms.ModelChoiceField(
        queryset=Location.objects.filter(is_active=True), 
        label="Select Location",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    
