"""Tests for the select genres form."""
from django import forms
from django.test import TestCase
from clubs.forms import GenreForm
from django.contrib.auth.hashers import check_password
from clubs.models import User

class GenreFormTestCase(TestCase):
    """Unit tests of the sign up form"""

    fixtures = ["clubs/tests/fixtures/default_user.json"]

    def setUp(self):
        self.form_input = {
            'genres_preferences': [('Fiction'), ('Romance'), ('Horror'), ('Mystery'), ('Politics')]
        }

    def test_valid_sign_up(self):
        form = GenreForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessay_fields(self):
        form = GenreForm()
        self.assertIn('genres_preferences', form.fields)
        genre_field = form.fields['genres_preferences']
        self.assertTrue(isinstance(genre_field, forms.MultipleChoiceField))

    def test_form_uses_model_validation(self):
        self.form_input['genres_preferences'] = 'badinput'
        form = GenreForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = GenreForm(data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTrue(form.is_valid())
        # self.assertEqual(user.genres_preferences, [('Fiction'), ('Romance'), ('Horror'), ('Mystery'), ('Politics')])