from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club
from clubs.tests.helpers import reverse_with_next, LogInTester

class ShowClubTest(TestCase, LogInTester):
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.org')
        self.club = Club.objects.get(name='Booker')
        self.url = reverse('show_club', kwargs={'club_id': self.club.id})

    def test_show_club_url(self):
        self.assertEqual(self.url,f'/club/{self.club.id}')

    def test_get_show_club_with_valid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/show_club.html')
        self.assertContains(response, self.club.name)
        self.assertContains(response, self.club.location)

    def test_show_club_with_invalid_id(self):
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('show_club', kwargs={'club_id': self.club.id+9999})
        response = self.client.get(self.url)
        redirect_url = reverse('club_list')
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_show_club_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
