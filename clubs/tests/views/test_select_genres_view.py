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
        self.form_input = {
            'genres_preferences': [('Fiction'), ('Romance'), ('Horror'), ('Mystery'), ('Politics')]
        }
        self.invalid_form_input = {
            'genres_preferences': [('Fiction'), ('Romance'), ('Horror'), ('Mystery'), ('Politics'), ('Nonfiction', 'Nonfiction')]
        }
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

    def test_successful_select_genre_update(self):
        self.client.login(username=self.user.username, password="Password123")
        user_before_count = User.objects.count
        self.assertEqual(self.user.genres_preferences, [])
        response = self.client.post(self.url, self.form_input, follow = True)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'feed.html')
        user_after_count = User.objects.count
        self.assertEqual(user_before_count, user_after_count)
        #self.assertEqual(self.user.genres_preferences, [('Fiction'), ('Romance'), ('Horror'), ('Mystery'), ('Politics')])

    def test_unsuccessful_select_genres(self):
        self.client.login(username=self.user.username, password="Password123")
        user_before_count = User.objects.count
        self.assertEqual(self.user.genres_preferences, [])
        response = self.client.post(self.url, self.invalid_form_input, follow = True)
        self.assertEqual(response.status_code, 200)
        user_after_count = User.objects.count
        self.assertEqual(user_before_count, user_after_count)
        self.assertEqual(self.user.genres_preferences, [])
