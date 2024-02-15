from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput, EmailInput

from .models import Task

class CreateUserForm(UserCreationForm):

    password1 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password1'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password2'}))

    class Meta:

        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': TextInput(attrs={'placeholder': 'Last Name'}),
            'username': TextInput(attrs={'placeholder': 'Username'}),
            'email': EmailInput(attrs={'placeholder': 'E-mail'}),
        }


class LoginUserForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))


class BecomeAssigner(forms.Form):
    status = forms.BooleanField(widget=forms.CheckboxInput(attrs={'onclick':'this.form.submit();'}),required=False, label="Status")
