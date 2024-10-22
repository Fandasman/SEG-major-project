"""Test of the create club view"""
from django.test import TestCase
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from clubs.models import Club, User, Role


class CreateClubViewTestCase(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_clubs.json',]

    def setUp(self):
        self.url = reverse('create_club')
        self.user = User.objects.get(email='johndoe@example.org')
        self.form_input = {
            'name': 'test_club',
            'location': 'London',
            'description': 'this is the test club'
        }

    def test_create_club_url(self):
        self.assertEqual(reverse('create_club'), '/create_club/')

    def test_template_used_by_invite_view(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/create_club.html')

    def test_create_club_redirects_when_logged_out(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)

    def test_get_create_club(self):
        self.client.login(username = self.user.username, password = "Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/create_club.html')

    def test_create_club_with_too_many_created_clubs(self):
        club1 = Club.objects.create(name='club1')
        club2 = Club.objects.create(name='club2')
        club3 = Club.objects.create(name='club3')
        Role.objects.create(club=club1, user=self.user, role='CO')
        Role.objects.create(club=club2, user=self.user, role='CO')
        Role.objects.create(club=club3, user=self.user, role='CO')
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'You already own too many clubs!')

    def create_ownership_roles(self):
        Role.objects.create(
            user = self.user,
            club = Club.objects.get(id = 2),
            role = "CO"
        )
        Role.objects.create(
            user = self.user,
            club = Club.objects.get(id = 3),
            role = "CO"
        )
        Role.objects.create(
            user = self.user,
            club = Club.objects.get(id = 4),
            role = "CO"
        )

    def test_unsuccessful_create_club(self):
        self.form_input['name'] = ''
        self.form_input['location'] = ''
        self.form_input['description'] = 'a'* 501
        response = self.client.post(self.form_input)
        self.assertEqual(response.status_code, 404)

    def test_successful_create_club(self):
        self.client.login(username = self.user.username, password = "Password123")
        before_count = Club.objects.count()
        role_before_count = Role.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Club.objects.count()
        role_after_count = Role.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertEqual(role_after_count, role_before_count+1)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
