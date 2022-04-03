from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from django.shortcuts import redirect
<<<<<<< HEAD
from django.forms import Form,ChoiceField, CharField
from .models import Club, User, Book, Event, UserPost, Comment
=======
from bootstrap5.widgets import RadioSelectButtonGroup
from .models import BooksRatings, Club, User, Book, Event
from .helpers import get_genres
>>>>>>> 67c3ad16c9244813f45d373463c1cd385c351512


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
<<<<<<< HEAD
=======

>>>>>>> 67c3ad16c9244813f45d373463c1cd385c351512
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


class ClubBookForm(forms.ModelForm):
    """Form to update a club's current book."""

    class Meta:
        """Form options."""

    def is_valid(self):
        super().is_valid()
        try:
            user = User.objects.get(username=self.cleaned_data.get('username'))
            return True
        except ObjectDoesNotExist:
            return False



class GenreForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["genres_preferences"]
        genres_preferences = forms.MultipleChoiceField(
            choices=get_genres(),
            widget=forms.CheckboxInput(),
        )
        error_messages={'genres_preferences':
            {'max_choices': 'Try selecting just a few of your favourites. Keep it nice and simple!'}
        }

    def save(self):
        super().save(commit=False)
        genres_preferences = self.cleaned_data.get('genres_preferences')
        return genres_preferences


class RatingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['rating'].label = ""

    rating = forms.ChoiceField(
        choices=[(rating, rating) for rating in range(1,6)],
        widget=RadioSelectButtonGroup,
        initial=1,
        required = False
    )


    class Meta:
        model = BooksRatings
        fields = ["rating"]


class BookModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_title()

class EventForm(forms.ModelForm):
    """Form allowing a officer to create a new tournament model"""



    class Meta:
        """Form options."""
        model = Event
        fields = ['name', 'description', 'maxNumberOfParticipants','deadline','book','location']
        widgets = { 'description': forms.Textarea()}

        book = BookModelChoiceField(label ="Book",queryset = Book.objects.values_list('title',flat = True))



    def get_book_titles():
       for book in Book.objects.all():
           book_titles = book.name
       return book_titles

    def clean(self):
        pass
    def save(self, club_id,current_user):
        super().save(commit = False)
        event = Event.objects.create(
            name=self.cleaned_data.get('name'),
            description=self.cleaned_data.get('description'),
            maxNumberOfParticipants= self.cleaned_data.get('maxNumberOfParticipants'),
            deadline = self.cleaned_data.get('deadline'),
            book = self.cleaned_data.get('book'),
            club = Club.objects.get(id = club_id),
            organiser = current_user,
            location = self.cleaned_data.get('location')

        )
        event.save()
        return event

class UserPostForm(forms.ModelForm):
    """Form to ask user for post text.

    The post author must be by the post creator.
    """

    class Meta:
        """Form options."""

        model = UserPost
        fields = ['text']
        labels = {
            'text': ('Add post'),
        }
        widgets = {
            'Post': forms.Textarea(attrs={'rows':10, 'cols':10})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': ('Add comment'),
        }
        widgets = {
            'Comment': forms.Textarea(attrs={'rows':1, 'cols':1, 'style':'resize:none;'})
        }
class SearchForm(Form):
    FILTER_CHOICES = (
        ('books', 'Books'),
        ('users', 'Users'),
        ('clubs', 'Clubs'),
        ('all', 'All')
    )
    search = CharField(required=True)
    filter_field = ChoiceField(choices=FILTER_CHOICES)
