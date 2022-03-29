"""Tests of the home view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User

class HomeViewTestCase(TestCase):
    """Tests of the home view."""

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('home')
        self.user = User.objects.get(email='johndoe@example.org')

    def test_home_url(self):
        self.assertEqual(self.url,'/')

    def test_get_home(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_templates/home.html')
