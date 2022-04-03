from django.test import TestCase
from django.urls import reverse
from clubs.models import Club, User, Role, Message


class SendClubMessageViewTestCase(TestCase):
    fixtures = [
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username="johndoe")
        self.other_user = User.objects.get(username="janedoe")
        self.club = Club.objects.get(name='Booker')
        self.role = Role.objects.create(user=self.user, club=self.club, role="O")
        self.role = Role.objects.create(user=self.other_user, club=self.club, role="A")
        self.url = reverse('send_club_message')
        self.form_input = {
            'user_id': self.user.id,
            'club_id': self.club.id,
            'text': 'hello',
        }

    def test_send_club_message_url(self):
        self.assertEqual(self.url, f'/send_club_message/')

    def test_successful_send_club_message(self):
        self.client.login(username=self.user.username, password="Password123")
        before_count = Message.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Message.objects.count()
        self.assertEqual(after_count, before_count + 1)

    def test_club_member_can_send_messages(self):
        self.other_user.role = "M"
        self.client.login(username=self.other_user.username, password="Password123")
        before_count = Message.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Message.objects.count()
        self.assertEqual(after_count, before_count + 1)

    def test_user_not_in_club_cannot_send_messages(self):
        form_input = {
            'user_id': self.other_user.id,
            'club_id': self.club.id,
            'text': 'hello',
        }
        self.client.login(username=self.other_user.username, password="Password123")
        before_count = Message.objects.count()
        response = self.client.post(self.url, form_input, follow=True)
        after_count = Message.objects.count()
        self.assertNotEqual(after_count, before_count + 1)