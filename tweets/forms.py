from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import Textarea, CheckboxInput, PasswordInput
from .models import UserProfile, Tweet


# form used to register a user
class UserForm(UserCreationForm):
    "tried using the user creation form, didnt like it"
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]
        widgets = {
            # this sets the input text area
            "password": PasswordInput(),
        }

# form used to create and edit a post
class CreateForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = [
            "content",
            "link",
            "tags",
        ]
        widgets = {
            # this sets the input text area
            "content": Textarea(attrs={"cols": 60, "rows": 10}),
            "link": forms.TextInput(attrs={'placeholder': 'https://www.google.com'}),
            "tags": Textarea(attrs={"cols": 30, "rows": 5}),
        }


