"""Unit tests of the Edit Profile form."""
from django import forms
from django.test import TestCase
from clubs.forms import EditProfileForm
from clubs.models import User

class TestEditProfileForm(TestCase):
    """Unit tests of the Edit Profile form."""
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(email="johndoe@example.org")
        self.form_input = {
            'username': 'johndoe2',
            'first_name': 'John2',
            'last_name': 'Doe2',
            'email': 'johndoe2@example.org',
            'bio': 'New bio',
            }

    def test_form_has_necessary_fields(self):
        form = EditProfileForm()
        self.assertIn('username', form.fields)
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('bio', form.fields)


    def test_valid_user_form(self):
        form = EditProfileForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_uses_model_validation(self):
        self.form_input['email'] = 'bademailexample.org'
        form = EditProfileForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = EditProfileForm(instance=self.user, data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(self.user.username, 'johndoe2')
        self.assertEqual(self.user.first_name, 'John2')
        self.assertEqual(self.user.last_name, 'Doe2')
        self.assertEqual(self.user.email, 'johndoe2@example.org')
        self.assertEqual(self.user.bio, 'New bio')
