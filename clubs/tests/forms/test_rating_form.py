"""Tests for the select genres form."""
from django import forms
from django.test import TestCase
from clubs.forms import RatingForm
from clubs.models import User, Book, BooksRatings

class RatingFormTestCase(TestCase):
    """Unit tests of the RatingForm form"""

    fixtures = ["clubs/tests/fixtures/default_user.json",
                "clubs/tests/fixtures/default_book.json"]

    def setUp(self):
        self.user = User.objects.get(username = 'johndoe')
        self.book = Book.objects.get(id = 1)
        self.form_input = {
            'rating': 3
        }

    def test_valid_rating(self):
        form = RatingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessay_fields(self):
        form = RatingForm()
        self.assertIn('rating', form.fields)
        rating_field = form.fields['rating']
        self.assertTrue(isinstance(rating_field, forms.ChoiceField))

    def test_form_uses_model_validation(self):
        self.form_input['rating'] = 'badinput'
        form = RatingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_rating_higher_than_5(self):
        self.form_input['rating'] = 6
        form = RatingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_rating_lower_than_1(self):
        self.form_input['rating'] = 0
        form = RatingForm(data=self.form_input)
        self.assertFalse(form.is_valid())