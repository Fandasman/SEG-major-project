from django.test import TestCase
from django.core.exceptions import ValidationError
from clubs.models import User, Club, Role

class RoleModelTestCase(TestCase):
    """Unit tests for the role model."""

    fixtures = [
        "clubs/tests/fixtures/default_user.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/default_club.json",
        "clubs/tests/fixtures/other_clubs.json",
        "clubs/tests/fixtures/default_book.json",
        "clubs/tests/fixtures/default_applicant.json",
        "clubs/tests/fixtures/other_applicants.json",
    ]

    def setUp(self):
        self.club = Club.objects.get(id = 1)
        self.user = User.objects.get(username = 'johndoe')
        self.role = Role.objects.get(user = self.user)

    # User tests
    def test_user_is_not_blank(self):
        self.role.user=None
        self._assert_role_is_invalid()

    def test_user_does_not_have_to_be_unique(self):
        second_role = self._get_second_role()

        self.role.user = second_role.user
        self.role.club = Club.objects.get(id=3)
        self._assert_role_is_valid()

    def test_user_field_must_contain_a_user(self):
        self.role.user = self.user
        self._assert_role_is_valid()

    def test_role_is_deleted_upon_deleting_the_user_model(self):
        self.user.delete()
        with self.assertRaises(Role.DoesNotExist):
            Role.objects.get(pk = self.role.pk)
        self._assert_role_is_invalid()

    # Club tests
    def test_club_is_not_blank(self):
        self.role.club=None
        self._assert_role_is_invalid()

    def test_club_does_not_have_to_be_unique(self):
        second_role = self._get_second_role()
        self.role.club = second_role.club
        self._assert_role_is_valid()

    def test_club_field_must_contain_a_club(self):
        self.role.club = self.club
        self._assert_role_is_valid()

    def test_role_is_deleted_upon_deleting_the_club_model(self):
        self.club.delete()
        with self.assertRaises(Role.DoesNotExist):
            Role.objects.get(pk = self.role.pk)
        self._assert_role_is_invalid()

    # Role tests
    def test_role_is_not_blank(self):
        self.role.role = ''
        self._assert_role_is_invalid()

    def test_role_can_be_owner(self):
        self.role.role = "CO"
        self._assert_role_is_valid()

    def test_role_can_be_applicant(self):
        self.role.role = "A"
        self._assert_role_is_valid()

    def test_role_can_be_member(self):
        self.role.role = "M"
        self._assert_role_is_valid()

    def test_role_can_be_officer(self):
        self.role.role = "O"
        self._assert_role_is_valid()

    def test_role_wrong_input(self):
        self.role.role = "B"
        self._assert_role_is_invalid()

    def test_role_does_not_have_to_be_unique(self):
        second_role = self._get_second_role()
        self.role.role = second_role.role
        self._assert_role_is_valid()

    def test_role_unique_together(self):
        second_role = self._get_second_role()
        self.role.user = second_role.user
        self.role.club = second_role.club
        self._assert_role_is_invalid()

    def test_role_field_cannot_have_more_than_2_characthers(self):
        self.role.role = 'x'* 3
        self._assert_role_is_invalid()

    def test_role_field_should_have_less_than_3_characthers(self):
        self.role.role = 'x'* 2
        self._assert_role_is_invalid()

    def test_role_field_must_contain_values_from_role_choices(self):
        self.role.role = 'x'
        self._assert_role_is_invalid()

    # Test case assertions
    def _assert_role_is_valid(self):
        try:
            self.role.full_clean()
        except (ValidationError):
            self.fail('Test should be valid')

    def _assert_role_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.role.full_clean()

    # Create second role
    def _get_second_role(self):
        second_user = User.objects.get(id = 2)
        second_club = Club.objects.get(id = 2)
        second_role = Role.objects.create(
            user = second_user,
            club = second_club,
            role = "M"
        )
        return second_role
