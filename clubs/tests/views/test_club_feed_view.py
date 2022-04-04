"""Tests of the club feed view."""
from django.contrib import messages
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from clubs.forms import UserPostForm, Club
from clubs.models import User
from clubs.tests.helpers import reverse_with_next, create_posts


class FeedViewTestCase(TestCase):
    """Tests of the feed view."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/default_applicant.json',
        'clubs/tests/fixtures/other_members.json'

    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.club = Club.objects.get(id=1)
        self.url = reverse('club_feed', kwargs={'club_id': self.club.id})

    def test_feed_url(self):
        self.assertEqual(self.url,f'/club_feed/{self.club.id}/')

    def test_get_club_feed(self):
        self.client.login(username='janedoe', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/club_feed.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserPostForm))
        self.assertFalse(form.is_bound)

    def test_get_feed_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_feed_contains_posts_by_members_of_club(self):
        jane = User.objects.get(username='janedoe')
        self.client.login(username='janedoe', password='Password123')
        alice = User.objects.get(username='alicesmith')
        bob = User.objects.get(username='bobsmith')
        create_posts(jane, 100, 103, self.club)
        create_posts(alice, 200, 203, self.club)
        create_posts(bob, 300, 303, self.club)
        response = self.client.get(self.url)
        for count in range(100, 103):
            self.assertContains(response, f'Post__{count}')
        for count in range(200, 203):
            self.assertContains(response, f'Post__{count}')
        for count in range(300, 303):
            self.assertContains(response, f'Post__{count}')

    def test_applicants_cannot_access(self):
        self.client.login(username='johndoe', password='Password123')
        response = self.client.get(self.url)
        redirect_url = reverse('club_list')
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    def test_non_member_cannot_access(self):
        new_user = User.objects.create_user(
            username = 'test',
            email = 'test@testing.com',
            password = 'Password123'
        )
        new_user.save()
        self.client.login(username='test', password='Password123')
        response = self.client.get(self.url)
        redirect_url = reverse('club_list')
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
