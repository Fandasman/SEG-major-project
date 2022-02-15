"""Test of the create club view"""
from django.test import TestCase
from django.urls import reverse
from clubs.models import Club, User, Role


class CreateClubViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('create_club')
        self.user = User.objects.create_user(
            '@johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.org',
            password='Password123',
            bio='Hi, my name is John.'
        )
        self.form_input = {
            'name': 'test_club',
            'location': 'London',
            'description': 'this is the test club'
        }

    def test_create_club_url(self):
        self.assertEqual(reverse('create_club'), '/create_club/')

    def test_get_create_club(self):
        self.client.login(username = self.user.username, password = "Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_club.html')

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
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)