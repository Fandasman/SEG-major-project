from django.test import TestCase
from django.urls import reverse
from clubs.models import Club, User, Role, Book, Invitation, Message


class InviteViewTestCase(TestCase):
    fixtures = [
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/default_book.json',
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username="johndoe")
        self.other_user = User.objects.get(username="alicesmith")
        self.club = Club.objects.get(name='Booker')
        self.role = Role.objects.create(user=self.user, club=self.club, role="O")
        self.url = reverse('send_club_message')
        self.form_input = {
            'text': 'hello',
        }

"""
    def test_successful_send_club_message(self):
        self.role.refresh_from_db()
        self.client.login(username=self.user.username, password="Password123")
        before_count = Message.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Message.objects.count()
        #response_url = reverse('show_club', kwargs={"club_id": self.club.id})
        self.assertEqual(after_count, before_count+1)
        #self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
"""
