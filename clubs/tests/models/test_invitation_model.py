from django.test import TestCase
from django.core.exceptions import ValidationError
from clubs.models import User, Club, Invitation

class InvitationTestCase(TestCase):
    """Unit tests for the invitation model."""

    fixtures = [
        "clubs/tests/fixtures/default_user.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/default_club.json",
        "clubs/tests/fixtures/other_clubs.json"
    ]

    def setUp(self):
        self.club = Club.objects.get(id = 1)
        self.user = User.objects.get(username = 'johndoe')
        self.invitation = Invitation.objects.create(
            user = self.user,
            club = self.club,
            status = "A"
        )

    # User tests
    def test_user_is_not_blank(self):
        self.invitation.user=None
        self._assert_invitation_is_invalid()

    def test_user_does_not_have_to_be_unique(self):
        second_invitation = self._get_second_invitation()
        
        self.invitation.user = second_invitation.user
        self._assert_invitation_is_valid()

    def test_invitation_is_deleted_upon_deleting_the_user_model(self):
        self.user.delete()
        with self.assertRaises(Invitation.DoesNotExist):
            Invitation.objects.get(pk = self.invitation.pk)
        self._assert_invitation_is_invalid()

    # Club tests
    def test_club_is_not_blank(self):
        self.invitation.club=None
        self._assert_invitation_is_invalid()

    def test_club_does_not_have_to_be_unique(self):
        second_invitation = self._get_second_invitation()
        self.invitation.club = second_invitation.club
        self._assert_invitation_is_valid()

    def test_invitation_is_deleted_upon_deleting_the_user_model(self):
        self.club.delete()
        with self.assertRaises(Invitation.DoesNotExist):
            Invitation.objects.get(pk = self.invitation.pk)
        self._assert_invitation_is_invalid()

    # Status tests
    def test_status_is_not_blank(self):
        self.invitation.status = ''
        self._assert_invitation_is_invalid()

    def test_status_can_be_pending(self):
        self.invitation.status = "P"
        self._assert_invitation_is_valid()

    def test_status_can_be_accepted(self):
        self.invitation.status = "A"
        self._assert_invitation_is_valid()
    
    def test_status_can_be_rejected(self):
        self.invitation.status = "R"
        self._assert_invitation_is_valid()

    def test_status_wrong_input(self):
        self.invitation.status = "B"
        self._assert_invitation_is_invalid()

    def test_status_does_not_have_to_be_unique(self):
        second_invitation = self._get_second_invitation()
        self.invitation.status = second_invitation.status
        self._assert_invitation_is_valid()

    # Test invitation must be a unique together entry.
    def test_invitation_unique_together(self):
        second_invitation = self._get_second_invitation()
        self.invitation.user = second_invitation.user
        self.invitation.club = second_invitation.club
        self._assert_invitation_is_invalid()

    
    # Test case assertions
    def _assert_invitation_is_valid(self):
        try:
            self.invitation.full_clean()
        except (ValidationError):
            self.fail('Test should be valid')

    def _assert_invitation_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.invitation.full_clean()

    # Create second invitation
    def _get_second_invitation(self):
        second_user = User.objects.get(id = 2)
        second_club=Club.objects.get(id = 2)
        second_invitation = Invitation.objects.create(
            user = second_user,
            club = second_club,
            status = "R"
        )
        return second_invitation