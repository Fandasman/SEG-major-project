from django.test import TestCase
from django.core.exceptions import ValidationError
from clubs.models import User, Club, Invitation


class InvitationModelTestCase(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/default_invitation.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username="johndoe")
        self.club = Club.objects.get(name="Booker")
        self.invitation = Invitation.objects.get(user=self.user)

    def test_user_field_must_contain_a_user(self):
        self.invitation.user = self.user
        self._assert_invitation_is_valid()

    def test_user_field_cannot_be_blank(self):
        self.invitation.user.delete()
        self._assert_invitation_is_invalid()

    def test_club_field_must_contain_a_club(self):
        self.invitation.club = self.club
        self._assert_invitation_is_valid()

    def test_club_field_cannot_be_empty(self):
        self.invitation.club.delete()
        self._assert_invitation_is_invalid()

    def test_status_field_must_contain_values_from_status_choices(self):
        self.invitation.status = 'x'
        self._assert_invitation_is_invalid()

    def _assert_invitation_is_valid(self):
        try:
            self.invitation.full_clean()
        except (ValidationError):
            self.fail('Test should be valid')

    def _assert_invitation_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.invitation.full_clean()