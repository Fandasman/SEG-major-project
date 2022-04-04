from django.test import TestCase
from django.core.exceptions import ValidationError
from clubs.models import User, Club

class ClubModelTestCase(TestCase):
    """Unit tests of the club model."""

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_clubs.json',
                ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(username='johndoe')
        self.club = Club.objects.get(name="Booker")

# Name tests.
    def test_name_is_not_blank(self):
        self.club.name=''
        self._assert_club_is_invalid()

    def test_name_must_be_unique(self):
        second_club=Club.objects.get(name="Clubber")
        self.club.name=second_club.name
        self._assert_club_is_invalid()

    def test_name_contains_whitespace(self):
        self.club.name = "Booker "
        self._assert_club_is_valid()

    def test_name_contains_number(self):
        self.club.name = "B00ker"
        self._assert_club_is_valid()

    def test_name_can_have_less_than_50_characters(self):
        self.club.name='x' * 50
        self._assert_club_is_valid()

    def test_name_cannot_have_more_than_50_characters(self):
        self.club.name='x' * 51
        self._assert_club_is_invalid()

# Location tests.
    def test_location_cannot_be_blank(self):
        self.club.location = ''
        self._assert_club_is_invalid()

    def test_location_can_have_less_than_100_characters(self):
        self.club.location='x' * 100
        self._assert_club_is_valid()

    def test_location_cannot_have_more_than_100_characters(self):
        self.club.location='x' * 101
        self._assert_club_is_invalid()

    def test_location_does_not_have_to_be_unique(self):
        second_club=Club.objects.get(name="Clubber")
        self.club.location=second_club.location
        self._assert_club_is_valid()

# Description tests.
    def test_description_cannot_be_blank(self):
        self.club.description=''
        self._assert_club_is_invalid()

    def test_description_does_not_need_to_be_unique(self):
        second_club=Club.objects.get(name="Clubber")
        self.club.description = second_club.description
        self._assert_club_is_valid()

    def test_description_may_have_500_chars(self):
        self.club.bio='x' * 500
        self._assert_club_is_valid()

    def test_description_cannot_have_over_500_chars(self):
        self.club.description='x' * 501
        self._assert_club_is_invalid()

# Test case assertions
    def _assert_club_is_valid(self):
        try:
            self.club.full_clean()
        except (ValidationError):
            self.fail('Test should be valid')

    def _assert_club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.club.full_clean()
