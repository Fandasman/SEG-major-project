from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Message


class SendUserMessageViewTestCase(TestCase):

    fixtures = [
                'clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                ]

    def setUp(self):
        self.url = reverse('send_user_message')
        self.user = User.objects.get(username = 'johndoe')
        self.receiver = User.objects.get(username='janedoe')
        self.form_input ={
            'receiver_id': self.receiver.id,
            'text': 'hello'
        }

    def test_send_user_message_url(self):
        self.assertEqual(self.url, f'/send_user_message/')

    def test_successful_send_user_message(self):
        self.client.login(username=self.user.username, password="Password123")
        before_count = Message.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Message.objects.count()
        self.assertEqual(after_count, before_count + 1)

    def test_unsuccessful_send_user_message(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)