from django.test import TestCase
from django.core.exceptions import ValidationError
from clubs.models import User, Club, Event, Book
from datetime import date, timedelta

class EventModelTestCase(TestCase):


    fixtures = [
    'clubs/tests/fixtures/default_user.json',
    'clubs/tests/fixtures/default_club.json',
    'clubs/tests/fixtures/other_users.json',
    'clubs/tests/fixtures/default_book.json',
    'clubs/tests/fixtures/default_event.json',
    'clubs/tests/fixtures/other_event.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username="alicesmith")
        self.club = Club.objects.get(name="Booker")
        self.event = Event.objects.get(name="DefaultEvent")
        self.book = Book.objects.get(isbn = "9783161484100")
        self.event.deadline = date.today()

    #Name tests
    def test_name_cannot_be_blank(self):
        self.event.name = ""
        self._assert_event_is_invalid()

    def test_name_must_be_unique(self):
        second_event = Event.objects.get(name="NewEvent")
        self.event.name =second_event.name
        self._assert_event_is_invalid()

    def test_name_must_have_lesss_than_51_characters(self):
        self.event.name = 'c' * 50
        self._assert_event_is_valid()

    def test_name_cannot_have_more_than_50_characters(self):
        self.event.name = 'c' * 51
        self._assert_event_is_invalid()

    def test_name_cannot_be_blank(self):
        self.event.name =''
        self._assert_event_is_invalid()

    #Test descripiton
    def test_description_must_have_lesss_than_521_characters(self):
        self.event.descripiton = 'c' * 520
        self._assert_event_is_valid()

    def test_description_cannot_have_more_than_520_characters(self):
        self.event.description = "x" * 521
        self._assert_event_is_invalid()

    def test_description_cannot_be_blank(self):
        self.event.description =''
        self._assert_event_is_invalid()

    #Test number of participants field
    def test_max_number_of_participants_cannot_be_more_than_96(self):
        self.event.maxNumberOfParticipants = 97
        self._assert_event_is_invalid()

    def test_max_number_of_participants_must_be_smaller_than_97(self):
        self.event.maxNumberOfParticipants = 96
        self._assert_event_is_valid()

    def test_min_number_of_participants_must_be_more_than_1(self):
        self.event.maxNumberOfParticipants = 2
        self._assert_event_is_valid()

    def test_min_number_of_participants_cannot_be_less_than_2(self):
        self.event.maxNumberOfParticipants = 1
        self._assert_event_is_invalid()

    #Test event location field
    def test_location_cannot_be_blank(self):
        self.event.location = ''
        self._assert_event_is_invalid()

    def test_location_cannot_have_more_than_255_charachters(self):
        self.event.location = 'x' * 256
        self._assert_event_is_invalid()

    def test_location_should_have_less_than_256_charachters(self):
        self.event.location = 'x' * 255
        self._assert_event_is_valid()

    #Test club field
    def test_club_field_must_contain_a_club(self):
        self.event.club = self.club
        self._assert_event_is_valid()

    def test_club_field_cannot_be_blank(self):
        self.event.club.delete()
        self._assert_event_is_invalid()

    #Test organiser
    def test_organiser_field_must_contain_a_user(self):
        self.event.user = self.user
        self._assert_event_is_valid()

    def test_organiser_field_cannot_be_blank(self):
        self.event.organiser.delete()
        self._assert_event_is_invalid()


    def _assert_event_is_valid(self):
        try:
            self.event.full_clean()
        except (ValidationError):
            self.fail('Test should be valid')

    def _assert_event_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.event.full_clean()
