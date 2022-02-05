from django import forms
from django.core.validators import RegexValidator
from .models import User, Club
from django.contrib.auth import authenticate

class LogInForm(forms.Form):
    email = forms.EmailField(required=True, label = "email")
    # Tried to make email not case senstive.
    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     return data.lower()
    password = forms.CharField(label = "Password", widget = forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user"""
        user = None
        if self.is_valid():
            username = self.cleaned_data.get('email').lower()
            password = self.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
        return user