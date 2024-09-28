from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, JobApplication, InternshipApplication, Job, Internship
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm



class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'age', 'phone_number']

    
class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['additional_details']

class InternshipApplicationForm(forms.ModelForm):
    class Meta:
        model = InternshipApplication
        fields = ['additional_details']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'domain_name']

class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = ['title', 'description', 'location', 'domain_name']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Include fields you want to allow editing

    def __init__(self, *args, **kwargs):
        # Pass any additional keyword arguments
        super().__init__(*args, **kwargs)
        # Customize form fields here if needed
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']