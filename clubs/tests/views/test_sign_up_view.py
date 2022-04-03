"""Tests for the sign up view."""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from clubs.forms import SignUpForm
from django.urls import reverse
from clubs.models import User
from clubs.tests.helpers import LogInTester

class SignUpViewTestCase(TestCase, LogInTester):

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('sign_up')
        self.form_input = {
            'username': 'janedoe',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.com',
            'bio': 'Hi, my name is Jane.',
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
        }
        self.user = User.objects.get(username='johndoe')


    def test_sign_up_url(self):
        self.assertEqual(self.url,'/sign_up/')


    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_templates/sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    def test_unsuccesful_sign_up(self):
        self.form_input['email'] = 'BAD_USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_templates/sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_successful_sign_up(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow = True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        response_url = reverse('select_genres')
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'select_genres.html')
        user = User.objects.get(username = 'janedoe')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.com')
        self.assertEqual(user.bio, 'Hi, my name is Jane.')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())

    # def test_post_sign_up_redirects_when_logged_in(self):
    #     self.client.login(username = 'johndoe@example.org', password='Password123')
    #     before_count = User.objects.count()
    #     response = self.client.post(self.url, self.form_input, follow=True)
    #     after_count = User.objects.count()
    #     self.assertEqual(after_count, before_count)
    #     redirect_url = reverse('club_list')
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response,'club_list.html')

    # def test_get_sign_up_redirects_when_logged_in(self):
    #     self.client.login(username = 'johndoe@example.org', password='Password123')
    #     response = self.client.get(self.url, follow=True)
    #     response_url = reverse('club_list')
    #     self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response,'club_list.html')
