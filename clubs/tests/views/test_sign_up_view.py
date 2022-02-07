# """Tests for the sign up view."""
# from django.contrib.auth.hashers import check_password
# from django.test import TestCase
# from clubs.forms import SignUpForm
# from django.urls import reverse
# from clubs.models import User
# from clubs.tests.helpers import LogInTester
#
# class SignUpViewTestCase(TestCase, LogInTester):
#
#     fixtures = ['clubs/tests/fixtures/default_user.json']
#
#     def setUp(self):
#         self.url = reverse('sign_up')
#         self.form_input = {
#             'first_name':'Jane',
#             'last_name':'Doe',
#             'email':'Johndoe@example.org',
#             'bio':'my bio',
#             'new_password':'Password123',
#             'password_confirmation':'Password123',
#         }
#         self.user = ClubUser.objects.get(email='johndoe@example.org')
#
#
#     def test_sign_up_url(self):
#         self.assertEqual(self.url,'/sign_up/')
#
#
#     def test_get_sign_up(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'sign_up.html')
#         form = response.context['form']
#         self.assertTrue(isinstance(form, SignUpForm))
#         self.assertFalse(form.is_bound)
#
#     def test_get_sign_up_redirects_when_logged_in(self):
#         self.client.login(username = 'johndoe@example.org', password='Password123')
#         response = self.client.get(self.url, follow=True)
#         response_url = reverse('club_list')
#         self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
#         self.assertTemplateUsed(response,'club_list.html')
#
#     def test_unsuccesful_sign_up(self):
#         self.form_input['email'] = 'BAD_USERNAME'
#         before_count = ClubUser.objects.count()
#         response = self.client.post(self.url, self.form_input)
#         after_count = ClubUser.objects.count()
#         self.assertEqual(after_count, before_count)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'sign_up.html')
#         form = response.context['form']
#         self.assertTrue(isinstance(form, SignUpForm))
#         self.assertTrue(form.is_bound)
#         self.assertFalse(self._is_logged_in())
#
#     def test_succesful_sign_up(self):
#         before_count = ClubUser.objects.count()
#         response = self.client.post(self.url, self.form_input, follow=True)
#         after_count = ClubUser.objects.count()
#         self.assertEqual(after_count, before_count+1)
#         response_url = reverse('club_list')
#         self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
#         self.assertTemplateUsed(response, 'club_list.html')
#         self.assertEqual(self.user.first_name,'John')
#         self.assertEqual(self.user.last_name,'Doe')
#         self.assertEqual(self.user.email,'johndoe@example.org')
#         self.assertEqual(self.user.bio,"Hello, I'm John Doe.")
#         self.assertEqual(self.user.personal_statement,'This is the personal statement.')
#         self.assertEqual(self.user.experience_level,2)
#         self.assertEqual(self.user.avatar,'defaultAvatar.jpg')
#         is_password_correct = check_password('Password123', self.user.password)
#         self.assertTrue(is_password_correct)
#         self.assertTrue(self._is_logged_in())
#
#     def test_post_sign_up_redirects_when_logged_in(self):
#         self.client.login(username = 'johndoe@example.org', password='Password123')
#         before_count = ClubUser.objects.count()
#         response = self.client.post(self.url, self.form_input, follow=True)
#         after_count = ClubUser.objects.count()
#         self.assertEqual(after_count, before_count)
#         redirect_url = reverse('club_list')
#         self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
#         self.assertTemplateUsed(response,'club_list.html')
