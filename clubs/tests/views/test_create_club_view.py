"""Test of the create club view"""
from django.test import TestCase
from django.urls import reverse

from clubs.forms import CreateClubForm
from clubs.models import Club
#from clubs.forms import CreateClubForm

class CreateClubViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('create_club')
        self.form_input = {
            'name': 'test_club',
            'description': 'this is the test club'
        }

    def test_create_club_url(self):
        self.assertEqual(reverse('create_club'), '/create_club/')

    def test_get_create_club(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_club.html')

    def test_unsuccessful_create_club(self):
        self.form_input['name'] = ''
        self.form_input['description'] = 'a'* 501
        response = self.client.post(self.form_input)
        self.assertEqual(response.status_code, 404)

    def test_successful_create_club(self):
        before_count = Club.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)