from django.test import TestCase
from django.core.exceptions import ValidationError
from clubs.models import User, Club, Role

class RoleModelTestCase(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
    'clubs/tests/fixtures/default_club.json',
    'clubs/tests/fixtures/other_users.json',
    'clubs/tests/fixtures/default_book.json',
    'clubs/tests/fixtures/default_applicant.json',
    'clubs/tests/fixtures/other_applicants.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username = "johndoe")
        self.club = Club.objects.get(name = "Booker")
        self.role = Role.objects.get(user = self.user)

    #Test user field
    def test_user_field_must_contain_a_user(self):
        self.role.user = self.user
        self._assert_role_is_valid()

    def test_user_field_cannot_be_blank(self):
        self.role.user.delete()
        self._assert_role_is_invalid()

    #Test club field
    def test_club_field_must_contain_a_club(self):
        self.role.club = self.club
        self._assert_role_is_valid()

    def test_club_field_cannot_be_empty(self):
        self.role.club.delete()
        self._assert_role_is_invalid()

    #Test role field
    def test_role_field_cannot_have_more_than_2_characthers(self):
        self.role.role = 'x'* 3
        self._assert_role_is_invalid()

    def test_role_field_should_have_less_than_3_characthers(self):
        self.role.role = 'x'* 2
        self._assert_role_is_invalid()

    def test_role_field_must_contain_values_from_role_choices(self):
        self.role.role = 'x'
        self._assert_role_is_invalid()


    def _assert_role_is_valid(self):
        try:
            self.role.full_clean()
        except (ValidationError):
            self.fail('Test should be valid')

    def _assert_role_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.role.full_clean()
