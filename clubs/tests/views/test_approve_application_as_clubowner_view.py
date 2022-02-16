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
        self.user = User.objects.get(email='alicesmith@example.org')
        self.member_user = User.objects.get(email='johndoe@example.org')
        self.role_user = Role.objects.get(user=self.member_user)
        self.url = reverse('accept_applicant_as_owner',kwargs={'club_id':self.club.id,'member_id':self.member_user.id})


    def test_approve_applicatin_as_CO_url(self):
        self.assertEqual(self.url,f'/accept_applicant/{self.club.id}/{self.member_user.id}')

    def test_get_approve_application_as_CO_is_forbidden(self):
        self.client.login(username = self.user.email, password='Password123')
        role_count_before = Role.objects.count()
        response = self.client.get(self.url, follow = True)
        role_count_after = Role.objects.count()
        self.assertEqual(role_count_after, role_count_before)
        self.assertEqual(response.status_code, 403)

    def test_unsuccessful_approve_the_application(self):
        pass

    def test_successful_approve_the_application(self):
        self.client.login(username=self.user.email, password='Password123')
        """member_user = User.objects.get(email='johndoe@example.org')
        applicant_user = Role.objects.get(user = self.member_user)"""
        before_count = Role.objects.count()
        response = self.client.post(self.url, follow=True)
        after_count = Role.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'memberList.html')
        self.role_user.refresh_from_db()
        self.assertEqual(self.role_user.role, 'M')

    def test_post_new_post_redirects_when_not_logged_in(self):
        user_count_before = Role.objects.count()
        redirect_url = reverse('log_in')
        response = self.client.post(self.url,follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        user_count_after = Role.objects.count()
        self.assertEqual(user_count_after, user_count_before)
