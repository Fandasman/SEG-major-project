from django import forms
from django.test import TestCase
from clubs.forms import SearchForm
from clubs.models import User

class TestEditProfileForm(TestCase):
    """Unit tests of the Edit Profile form."""
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username = 'johndoe')
        self.form_input = {'search': 'flowers',
                            'filter_field' : 'books'    }



    def test_form_has_necessary_fields(self):
        form = SearchForm()
        self.assertIn('search', form.fields)
        self.assertIn('filter_field', form.fields)

    def test_valid_search_form(self):
        form = SearchForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_invalid_search_form(self):
        self.form_input['search'] = ''
        form = SearchForm(data=self.form_input)
        self.assertFalse(form.is_valid())
