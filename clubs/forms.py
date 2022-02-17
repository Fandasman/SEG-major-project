from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from django.shortcuts import redirect

from .models import Club, User, Book


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email','bio']
        widgets = { 'bio': forms.Textarea()}
    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
        regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
        message='Password must contain an uppercase character, a lowercase '
            'character and a number'
        )]
    )
    password_confirmation = forms.CharField(label = 'Password confirmation', widget = forms.PasswordInput())



    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'confirmation does not match password.')

    def save(self):
        super().save(commit=False)
        user = User.objects.create_user(
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            username = self.cleaned_data.get('username'),
            email=self.cleaned_data.get('email'),
            bio=self.cleaned_data.get('bio'),
            password=self.cleaned_data.get('new_password'),
        )
        return user

class LogInForm(forms.Form):
    username = forms.CharField(required=True, label = "Username")

    # Tried to make email not case senstive.
    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     return data.lower()
    password = forms.CharField(label = "Password", widget = forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user"""
        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username').lower()
            password = self.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
        return user

class ClubForm(forms.ModelForm):
    """Form allowing a user to create a new club model"""

    class Meta:
        """Form options."""
        model = Club
        fields = ['name', 'location', 'description']
        widgets = { 'description': forms.Textarea() }


    def save(self):
        super().save(commit=False)
        club = Club.objects.create(
            name=self.cleaned_data.get('name'),
            location=self.cleaned_data.get('location'),
            description = self.cleaned_data.get('description')
        )
        return club


class EditProfileForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'bio']
        widgets = { 'bio': forms.Textarea()}


class SetClubBookForm(forms.Form):
    book_title = forms.CharField(max_length=50, required=True, label="book title")
    club_name = forms.CharField(max_length=50, required=True, label="club name")

    def get_book(self):
        try:
            book = Book.objects.get(title=self.cleaned_data.get('book_title'))
            return book
        except ObjectDoesNotExist:
            redirect('set_club_book')

    def get_club(self):
        try:
            club = Club.objects.get(name=self.cleaned_data.get('club_name'))
            return club
        except ObjectDoesNotExist:
            redirect('set_club_book')
