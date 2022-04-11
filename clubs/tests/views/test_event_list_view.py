from django.test import TestCase
from django.urls import reverse
from clubs.models import Club, User, Role, Book, Event


class EventListTestCase(TestCase):

    fixtures = ['clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_applicant.json',
                'clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_applicants.json',
                'clubs/tests/fixtures/default_book.json',
                'clubs/tests/fixtures/default_event.json'
                ]

    def setUp(self):
        self.club = Club.objects.get(name = 'Booker')
        self.user = User.objects.get(username = 'alicesmith')
        self.url = reverse('events_list', kwargs={'club_id': self.club.id})
        self.event = Event.objects.get(name = "DefaultEvent")

    def test_template_used_by_event_list_view(self):
        self.client.login(username = self.user.username, password='Password123')
        response = self.client.get(self.url, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/events_list.html')

    def test_redirect_when_ther_are_no_events(self):
        self.client.login(username = self.user.username, password='Password123')
        self.event.delete()
        redirect_url = reverse('club_list')
        response = self.client.get(self.url,follow=True)
        self.assertRedirects(response, redirect_url,
                status_code=302, target_status_code=200, fetch_redirect_response=True
            )
