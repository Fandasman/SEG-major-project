"""Tests of the select_genre view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User
from ..helpers import LogInTester, reverse_with_next

class SelectGenreViewTestCase(TestCase, LogInTester):
    """Tests of the select_genre view."""

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('select_genres')
        self.user = User.objects.get(username='johndoe')

    def test_select_genre_url(self):
        self.assertEquals(self.url, "/select_genres/")

    def test_select_genre_redirects_when_logged_out(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)

    def test_get_select_genre_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("select_genres.html")