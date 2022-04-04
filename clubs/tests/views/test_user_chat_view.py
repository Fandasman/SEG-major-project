from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Message


class UserChatViewTestCase(TestCase):

    fixtures = [
                'clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                ]

    def setUp(self):
        self.url = reverse('send_user_message')
        self.user = User.objects.get(username='johndoe')
        self.receiver = User.objects.get(username='janedoe')
        self.url = reverse('user_chat', kwargs={'receiver_id': self.receiver.id})

    def test_template_used_by_user_chat_view(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_templates/user_chat.html')
