from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Message, Club


class GetClubMessageViewTestCase(TestCase):

    fixtures = [
                'clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_message.json',
                ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.receiver = User.objects.get(username='janedoe')
        self.message = Message.objects.get(id=1)
        self.club = Club.objects.get(id=1)
        self.url = reverse('get_club_messages', kwargs={'club_id': self.club.id})
        self.form_input ={
            'club_id': self.club.id,
            'text': 'hello'
        }

    def test_get_club_message_url(self):
        self.assertEqual(self.url, '/get_club_messages/1/',)

    def test_successful_get_club_message(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'messages':
                 [{
                     'text': 'hello',
                     'username': 'johndoe'
                 }]
            }
        )
