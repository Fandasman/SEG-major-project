'''unit test of the create club form'''
from django.test import TestCase
from clubs.forms import CreateClubForm
from clubs.models import Club, User


class CreateClubFormTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            '@johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.org',
            password='Password123',
            bio='Hi, my name is John.'
        )
        self.form_input = {
            'name': 'test_club',
            'location': 'London',
            'description': 'this is the test club'
        }

    def test_valid_create_club_form(self):
        form = CreateClubForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = CreateClubForm()
        self.assertIn('name', form.fields)
        self.assertIn('location', form.fields)
        self.assertIn('description', form.fields)

    def test_form_uses_model_validation(self):
        self.form_input['name'] = ''
        self.form_input['location'] = ''
        self.form_input['description'] = 'a' * 501
        form = CreateClubForm(data= self.form_input)
        self.assertFalse(form.is_valid())
