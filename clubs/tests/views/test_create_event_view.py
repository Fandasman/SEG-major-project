from django.test import TestCase
from django.urls import reverse
from clubs.models import Club, User, Role, Book, Event
from datetime import date, timedelta


class CreateEventViewTestCase(TestCase):


    fixtures = ['clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_applicant.json',
                'clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_applicants.json',
                'clubs/tests/fixtures/default_book.json'
                ]

    def setUp(self):
        self.url = reverse('create_event', kwargs={'club_id':1})
        self.user = User.objects.get(username = 'alicesmith')
        self.book = Book.objects.get(isbn = '9783161484100')
        self.club = Club.objects.get(name = 'Booker')
        self.form_input ={
            'name': 'KCL event',
            'maxNumberOfParticipants':20,
            'deadline': date.today(),
            'book': self.book,
            'location': 'London',
            'description':"Book Club for KCL informatics students.",
            'organiser': self.user,
            'club' : self.club
        }


    def test_create_event_url(self):
        self.assertEqual(self.url, f'/club_event_creation/{self.club.id}/')

    def test_get_create_event(self):
        self.client.login(username = self.user.username, password = "Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/create_event.html')

    def test_unsuccessful_event_creation(self):
        self.form_input['name'] = ''
        self.form_input['location'] = ''
        self.form_input['description'] = 'a'* 501
        self.form_input['book'] = ''
        self.form_input['deadline'] = date.today() - timedelta(days =1)
        response = self.client.post(self.form_input)
        self.assertEqual(response.status_code, 404)
