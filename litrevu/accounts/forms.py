from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class SignupForm(UserCreationForm):
    """
    A form for creating new users. Includes all the required fields, plus a repeated password.

    :param model: The model that will be used to create the form.
    :type model: User
    :param fields: The fields that will be included in the form.
    :type fields: tuple of str
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
