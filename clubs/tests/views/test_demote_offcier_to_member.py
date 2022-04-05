
"""Test for approve the application as clubowner view"""
from django.test import TestCase
from clubs.models import Club, Role, User
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next


class ApproveTheApplicationAsCOTestCase(TestCase):


    fixtures = ['clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_applicant.json',
                'clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_applicants.json',
                'clubs/tests/fixtures/other_clubs.json']

    def setUp(self):
        self.club = Club.objects.get(name='Booker')
        self.owner = User.objects.get(email='bobsmith@example.org')
        self.officer = User.objects.get(username='alicesmith')
        self.role_user = Role.objects.get(user=self.officer)
        self.url = reverse('demotion',kwargs={'club_id':self.club.id,'member_id':self.officer.id})


    def test_approve_applicatin_as_CO_url(self):
        self.assertEqual(self.url,f'/demoted/{self.club.id}/{self.officer.id}')


    def test_demote_officer_to_member_as_CO(self):
        self.client.login(username = self.owner.username, password ="Password123")
        role_count_before_officers = Role.objects.filter(role = "O").count()
        role_count_before_members = Role.objects.filter(role = "M").count()
        response = self.client.post(self.url, follow=True)
        role_count_after_officers = Role.objects.filter(role = "O").count()
        role_count_after_members = Role.objects.filter(role = "M").count()
        self.assertEqual(role_count_after_officers, role_count_before_officers - 1)
        self.assertEqual(role_count_after_members, role_count_before_members  + 1)


    def test_demote_officer_to_member_as_CO_redirects_when_not_logged_in(self):
        user_count_before = Role.objects.count()
        redirect_url = reverse_with_next('login',self.url)
        response = self.client.post(self.url,follow=True)
        self.assertRedirects(response, redirect_url,
                status_code=302, target_status_code=200, fetch_redirect_response=True
            )
        user_count_after = Role.objects.count()
        self.assertEqual(user_count_after, user_count_before)

    def test_get_request_returns_HttpResponseForbidden(self):
        self.client.login(username = self.owner.username, password ="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 403)
