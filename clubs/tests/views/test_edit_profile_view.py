"""Tests for editing the profile view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.forms import EditProfileForm
from clubs.models import User
from clubs.tests.helpers import reverse_with_next

class TestEditProfileView(TestCase):
    """Test suite editing for the profile view."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username="johndoe")
        self.url = reverse('edit_profile')
        self.form_input = {
            'username': 'johndoe2',
            'first_name': 'John2',
            'last_name': 'Doe2',
            'email': 'johndoe2@example.org',
            'bio': 'New bio',
            }

    def test_get_profile_url(self):
        self.assertEqual(self.url, '/edit_profile/')

    def test_profile_redirects_when_logged_out(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)

    def test_get_edit_profile_for_users(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_templates/edit_profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditProfileForm))
        self.assertEqual(form.instance, self.user)

    def test_unsuccesful_profile_update(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['email'] = 'bademailexample.org'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_templates/edit_profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditProfileForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'johndoe')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'johndoe@example.org')
        self.assertEqual(self.user.bio, "Hi, I'm John.")

    def test_unsuccessful_profile_update_due_to_duplicate_email(self):
        self.client.login(username=self.user.username, password='Password123')
        self.second_user = User.objects.get(username="janedoe")
        self.form_input['email'] = 'jane@example.org'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_templates/edit_profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditProfileForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'johndoe')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'johndoe@example.org')
        self.assertEqual(self.user.bio, "Hi, I'm John.")

    def test_unsuccessful_profile_update_due_to_duplicate_username(self):
        self.client.login(username=self.user.username, password='Password123')
        self.second_user = User.objects.get(username="janedoe")
        self.form_input['username'] = 'janedoe'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_templates/edit_profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditProfileForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'johndoe')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'johndoe@example.org')
        self.assertEqual(self.user.bio, "Hi, I'm John.")


    def test_successful_profile_update(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        #messages_list = list(response.context['messages'])
        #self.assertEqual(len(messages_list), 2)
        #self.assertEqual(messages_list[0].level, messages.SUCCESS)
        #self.assertEqual(messages_list[1].level, messages.INFO)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'johndoe2')
        self.assertEqual(self.user.first_name, 'John2')
        self.assertEqual(self.user.last_name, 'Doe2')
        self.assertEqual(self.user.email, 'johndoe2@example.org')
        self.assertEqual(self.user.bio, 'New bio')

# Need to add mixins
    # def test_post_edit_profile_redirects_when_not_logged_in(self):
    #     redirect_url = reverse_with_next('login', self.url)
    #     response = self.client.post(self.url, self.form_input)
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
