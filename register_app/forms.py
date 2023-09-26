from django import forms
from .models import Location
from django.contrib.auth.models import User

class LocationForm(forms.ModelForm):
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
