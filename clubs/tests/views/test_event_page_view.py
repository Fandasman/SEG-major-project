"""Test for approve the application as clubowner view"""
from django.test import TestCase
from clubs.models import Club, Role, User,Event
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next


class EventPageTestCase(TestCase):

    fixtures = ['clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_applicant.json',
                'clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_applicants.json',
                'clubs/tests/fixtures/default_book.json',
                'clubs/tests/fixtures/default_event.json'
                ]

    def setUp(self):
        self.club = Club.objects.get(name='Booker')
        self.user = User.objects.get(email='alicesmith@example.org')
        self.event = Event.objects.get(name ="DefaultEvent")
        self.url = reverse('event_page',kwargs={'club_id':self.club.id,'event_id':self.event.id})


    def test_event_page_url(self):
        self.assertEqual(self.url,f'/event_page/{self.club.id}/{self.event.id}/')

    def test_template_used_by_event_page_view(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/event_page.html')
