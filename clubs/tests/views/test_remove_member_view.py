"""Test for approve the application as clubowner view"""
from django.test import TestCase
from clubs.models import Club, Role, User
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next


class RemoveMemberTestCase(TestCase):

    fixtures = ['clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_applicant.json',
                'clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_applicants.json',
                'clubs/tests/fixtures/other_clubs.json']

    def setUp(self):
        self.club = Club.objects.get(name='Booker')
        self.user = User.objects.get(email='alicesmith@example.org')
        self.member_user = User.objects.get(email='jane@example.org')
        self.role_user = Role.objects.get(user=self.member_user)
        self.url = reverse('removemember',kwargs={'club_id':self.club.id,'member_id':self.member_user.id})


    def test_remove_member_from_club_url(self):
        self.assertEqual(self.url,f'/removemember/{self.club.id}/{self.member_user.id}')

    def test_get_remove_member_from_club_is_forbidden(self):
        self.client.login(username = self.user.username, password='Password123')
        role_count_before = Role.objects.count()
        response = self.client.get(self.url, follow = True)
        role_count_after = Role.objects.count()
        self.assertEqual(role_count_after, role_count_before)
        self.assertEqual(response.status_code, 403)

    def test_unsuccessful_remove_the_member_from_the_club(self):
        pass

    def test_successful_remove_the_member_from_the_club(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = Role.objects.count()
        response = self.client.post(self.url, follow=True)
        after_count = Role.objects.count()
        self.assertEqual(after_count, before_count-1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/club_page.html')

    def test_post_new_post_redirects_when_not_logged_in(self):
        user_count_before = Role.objects.count()
        redirect_url = reverse('login')
        response = self.client.post(self.url,follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        user_count_after = Role.objects.count()
        self.assertEqual(user_count_after, user_count_before)
