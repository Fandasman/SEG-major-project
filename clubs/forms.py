from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from django.shortcuts import redirect

from .models import GENRE_CHOICES, BooksRatings, Club, User, Book



GENRE_CHOICES = [
    ('Fiction','Fiction'),
    ('Food and Drink','Food and Drink'),
    ('Science Fiction','Science Fiction'),
    ('Classics','Classics'),
    ('Nonfiction','Nonfiction'),
    ('Horror','Horror'),
    ('Mystery','Mystery'),
    ('Philosophy','Philosophy'),
    ('Business','Business'),
    ('Historical','Historical'),
    ('Romance','Romance'),
    ('Crime','Crime'),
    ('Womens Fiction','Womens Fiction'),
    ('Fantasy','Fantasy'),
    ('Young Adult','Young Adult'),
    ('Sequential Art','Sequential Art'),
    ('Politics','Politics'),
    ('Childrens','Childrens'),
    ('History','History'),
    ('Self Help','Self Help'),
    ('Humor','Humor'),
    ('Thriller','Thriller'),
    ('Autobiography','Autobiography'),
    ('Poetry','Poetry'),
    ('Short Stories','Short Stories'),
    ('Language','Language'),
    ('Science','Science'),
    ('Travel','Travel'),
    ('Parenting','Parenting'),
    ('Paranormal','Paranormal'),
    ('Biography','Biography'),
    ('Christian','Christian'),
    ('European Literature','European Literature'),
    ('Psychology','Psychology'),
    ('Adventure','Adventure'),
    ('Religion','Religion'),
    ('Holiday','Holiday'),
    ('Animals','Animals'),
    ('Christian Fiction','Christian Fiction'),
    ('Reference','Reference'),
    ('Spirituality','Spirituality'),
    ('Feminism','Feminism'),
    ('Health','Health'),
    ('Cultural','Cultural'),
    ('Adult Fiction','Adult Fiction'),
    ('Writing','Writing'),
    ('Realistic Fiction','Realistic Fiction'),
    ('Law','Law'),
    ('Art','Art'),
    ('Plays','Plays'),
    ('Relationships','Relationships'),
    ('Westerns','Westerns'),
    ('Sports','Sports')
]



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
    #club_name = forms.CharField(max_length=50, required=True, label="club name")

    def get_book(self):
            book = Book.objects.get(title=self.cleaned_data.get('book_title'))
            return book


   # def get_club(self):
           # club = Club.objects.get(name=self.cleaned_data.get('club_name'))
           # return club


    def is_valid(self):
        super().is_valid()
        try:
            book = Book.objects.get(title=self.cleaned_data.get('book_title'))
           # club = Club.objects.get(name=self.cleaned_data.get('club_name'))
            return True
        except ObjectDoesNotExist:
            return False

class InviteForm(forms.Form):
    model = User
    username = forms.CharField(max_length=50, required=True, label="username")

    def get_user(self):
        user = User.objects.get(username=self.cleaned_data.get('username'))
        return user

    def is_valid(self):
        super().is_valid()
        try:
            user = User.objects.get(username=self.cleaned_data.get('username'))
            return True
        except ObjectDoesNotExist:
            return False


    
class GenreForm(forms.ModelForm):

    genre_preferences = forms.MultipleChoiceField(
        choices=GENRE_CHOICES, 
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = User
        fields = ["genres_preferences"]


class RatingForm(forms.ModelForm):

    forms.ChoiceField(
        choices = [1,2,3,4,5]
    )

    class Meta:
        model = BooksRatings
        fields = ["rating"]

    # def clean(self):
    #     super().clean()
    #     rating = self.cleaned_data.get('rating')

  

