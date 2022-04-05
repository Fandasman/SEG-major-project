
"""Test for approve the application as clubowner view"""
from django.test import TestCase
from clubs.models import Club, Role, User
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next


class ClubMembersTestCase(TestCase):


    fixtures = ['clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_applicant.json',
                'clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_applicants.json',
                'clubs/tests/fixtures/other_clubs.json']

    def setUp(self):
        self.club = Club.objects.get(name='Booker')
        self.owner= User.objects.get(email='bobsmith@example.org')
        self.officer = User.objects.get(username='alicesmith')
        self.applicant = User.objects.get(username = 'johndoe')
        self.url = reverse('club_members',kwargs={'club_id':self.club.id})


    def test_club_members_url(self):
        self.assertEqual(self.url,f'/all_members/{self.club.id}/')

    def test_redirect_when_user_is_applicant(self):
        self.client.login(username = self.applicant.username, password ="Password123")
        redirect_url = reverse('club_list')
        response = self.client.get(self.url, follow = True)
        self.assertRedirects(response, redirect_url,
                    status_code=302, target_status_code=200, fetch_redirect_response=True
                )

    def test_redirect_when_user_is_not_part_of_club(self):
        self.client.login(username = self.applicant.username, password ="Password123")
        Role.objects.get(user = self.applicant, club = self.club).delete()
        redirect_url = reverse('club_list')
        response = self.client.get(self.url, follow = True)
        self.assertRedirects(response, redirect_url,
                    status_code=302, target_status_code=200, fetch_redirect_response=True
                )

    def test_template_used_to_render_club_members_page(self):
        self.client.login(username=self.officer.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/club_page.html')
