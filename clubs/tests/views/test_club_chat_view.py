from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club


class ClubChatViewTestCase(TestCase):

    fixtures = [
                'clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                ]

    def setUp(self):
        self.url = reverse('send_user_message')
        self.user = User.objects.get(username='johndoe')
        self.club = Club.objects.get(name='Booker')
        self.url = reverse('club_chat', kwargs={'club_id': self.club.id})

    def test_template_used_by_club_chat_view(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/club_chat.html')