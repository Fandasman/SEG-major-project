import clubs.models
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club, Role
from clubs.tests.helpers import LogInTester, reverse_with_next
from django.core.exceptions import FieldError


class TestSendApplicationView(TestCase, LogInTester):
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/default_member.json'
    ]

    def setUp(self):
        self.club = Club.objects.get(name="Booker")
        self.user = User.objects.get(username='janedoe')
        self.member = User.objects.get(username = 'johndoe')
        self.url = reverse('apply', kwargs={'club_id': self.club.id})

    def test_send_application_url(self):
        self.assertEqual(self.url,f'/apply/{self.club.id}')

    def test_get_send_application_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_send_application_forbidden_when_get(self):
        self.client.login(username='janedoe', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_get_send_application_to_club(self):
        self.client.login(username='janedoe', password='Password123')
        before_count = Role.objects.filter(club=self.club).count()
        response = self.client.post(self.url, follow=True)
        after_count = Role.objects.filter(club=self.club).count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_templates/club_list.html')

    def test_get_send_application_to_invalid_club(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('apply', kwargs={'club_id': self.club.id+9999})
        response = self.client.post(self.url, follow=True)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_templates/club_list.html')

    def test_redirected_to_club_list_when_existing_club_members_sends_application_again(self):
        self.client.login(username=self.member.username, password='Password123')
        response = self.client.post(self.url, follow=True)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_apply_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.post(self.url,follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
