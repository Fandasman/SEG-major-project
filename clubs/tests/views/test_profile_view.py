from django.test import TestCase
from django.urls import reverse
from clubs.models import User

class ProfileTestCase(TestCase):
    """Tests of the home view."""

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('profile')
        self.user = User.objects.get(email='johndoe@example.org')

    def test_profile_url(self):
        self.assertEqual(self.url, '/profile/')

    def test_get_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
#        self.assertContains(response, self.user.username)
#        self.assertContains(response, self.user.full_name)
#        self.assertContains(response, self.user.bio)


    def test_edit_profile_button(self):
        pass

#    def test_get_profile_redirects_when_logged_out(self):
#        self.client.login(username=self.user.username, password='Password123')
#        response = self.client.get(self.url, follow=True)
#        redirect_url = reverse('login')
#        self.assertRedirects(response, redirect_url, status_code=302,target_status_code=200)
#        self.assertTemplateUser(response, 'login')
