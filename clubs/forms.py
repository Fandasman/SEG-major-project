from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from .models import User
from .models import Club


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
    username = forms.CharField(required=True, label = "username")
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

class CreateClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'location', 'description']
        widgets = { 'description': forms.Textarea()}

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

        model = Club
        fields = ['current_book','book_page']
    
