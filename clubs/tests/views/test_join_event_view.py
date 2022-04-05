from django.test import TestCase
from django.urls import reverse
from clubs.models import Club, User, Role, Book, Event



class JoinEventTestCase(TestCase):

    fixtures = ['clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_applicant.json',
                'clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_applicants.json',
                'clubs/tests/fixtures/default_book.json',
                'clubs/tests/fixtures/default_event.json'
                ]

    def setUp(self):
        self.club = Club.objects.get(name = "Booker")
        self.event = Event.objects.get(name = "DefaultEvent")
        self.user  = User.objects.get(username = 'johndoe')
        self.url = reverse('join_event', kwargs ={'club_id': self.club.id, 'event_id': self.event.id})


    def test_join_event_is_succesful(self):
        self.client.login(username = self.user.username, password='Password123')
        before_count = self.event.participants.count()
        response = self.client.get(self.url, follow = True)
        after_count = self.event.participants.count()
        self.assertEqual(after_count,before_count + 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/events_list.html')

    def test_disjoin_event(self):
        self.client.login(username = self.user.username, password='Password123')
        before_count = self.event.participants.count()
        self.client.get(self.url, follow = True)
        response = self.client.get(self.url, follow = True)
        after_count = self.event.participants.count()
        self.assertEqual(after_count,before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/events_list.html')
