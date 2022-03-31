from django.test import TestCase
from django.urls import reverse
from clubs.models import Club, User, Role, Book, Event


class AddUserToIntrestedListFromEventPageTestCase(TestCase):


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
        self.url = reverse('interested_in_event_from_event_page', kwargs ={'club_id': self.club.id, 'event_id': self.event.id})

    def test_add_user_to_intrested_list(self):
        self.client.login(username = self.user.username, password='Password123')
        before_count = self.event.users_interested_in_event.count()
        response = self.client.get(self.url, follow = True)
        after_count = self.event.users_interested_in_event.count()
        self.assertEqual(after_count,before_count + 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/event_page.html')

    def test_remove_user_from_intrested_list(self):
        self.client.login(username = self.user.username, password='Password123')
        before_count = self.event.users_interested_in_event.count()
        self.client.get(self.url, follow = True)
        response = self.client.get(self.url, follow = True)
        after_count = self.event.users_interested_in_event.count()
        self.assertEqual(after_count,before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/event_page.html')
