from django.test import TestCase
from django.core.exceptions import ValidationError
from clubs.models import User, Club, Message


class MessageModelTestCase(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/default_message.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username="johndoe")
        self.receiver = User.objects.get(username="janedoe")
        self.club = Club.objects.get(name="Booker")
        self.message = Message.objects.get(user=self.user)

    def test_user_field_must_contain_a_user(self):
        self.message.user = self.user
        self._assert_message_is_valid()

    def test_user_field_cannot_be_blank(self):
        self.message.user.delete()
        self._assert_message_is_invalid()

    def test_text_length_cannot_exceed_20(self):
        self.message.text = "x"*21
        self._assert_message_is_invalid()

    def _assert_message_is_valid(self):
        try:
            self.message.full_clean()
        except (ValidationError):
            self.fail('Test should be valid')

    def _assert_message_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.message.full_clean()