from django import forms
from django.test import TestCase
from clubs.forms import EventForm
from clubs.models import Club, Book, User, Event
from datetime import date, timedelta


class EventCreationForm(TestCase):

    fixtures = ['clubs/tests/fixtures/default_book.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_users.json'
               ]

    def setUp(self):
        self.book = Book.objects.get(isbn = "9783161484100")
        self.club = Club.objects.get(name = "Booker")
        self.user = User.objects.get(username = "alicesmith")
        self.form_input = {
        'name': 'KCL event',
        'maxNumberOfParticipants':20,
        'deadline': date.today(),
        'book': self.book,
        'location': 'London',
        'description':"Book Club for KCL informatics students."
        }

    def test_form_contains_required_fields(self):
        form = EventForm()
        self.assertIn('name', form.fields)
        self.assertIn('location', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('maxNumberOfParticipants', form.fields)
        self.assertIn('deadline', form.fields)
        self.assertIn('book', form.fields)

    def test_form_accepts_valid_input(self):
        form = EventForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_name(self):
        self.form_input['name'] = ''
        form = EventForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_description(self):
        self.form_input['description'] = ''
        form = EventForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_location(self):
        self.form_input['location'] = ''
        form = EventForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_deadline(self):
        self.form_input['deadline'] = ''
        form = EventForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_book_field(self):
        self.form_input['book'] = ''
        form = EventForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_reject_past_dates_for_deadline(self):
        self.form_input['deadline'] = date.today() - timedelta(days=1)
        form = EventForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = EventForm(data=self.form_input)
        before_count = Event.objects.count()
        self.event = form.save(self.club.id,self.user)
        after_count = Event.objects.count()
        self.assertEqual(after_count, before_count+1)
        this_event = Event.objects.get(name = self.event.name)
        self.assertEqual(this_event.name,'KCL event')
        self.assertEqual(this_event.description,'Book Club for KCL informatics students.')
        self.assertEqual(this_event.location,"London")
        self.assertEqual(this_event.book.isbn, self.book.isbn)
        self.assertEqual(this_event.maxNumberOfParticipants, 20)
        self.assertEqual(this_event.deadline, date.today())
