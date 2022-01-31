from django.test import TestCase
from django.core.exceptions import ValidationError
from clubs.models import User

class UserModelTestCase(TestCase):
    fixtures = [
        "clubs/tests/fixtures/default_user.json",
        "clubs/tests/fixtures/other_users.json"
    ]

    def setUp(self):
        self.user = User.objects.get(username = 'johndoe')

# Username tests
    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_username_must_have_at_least_three_alphanumericals(self):
        self.user.username = 'us'
        self._assert_user_is_invalid()

    def test_username_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    def test_username_can_be_30_characters_long(self):
        self.user.username = 'x' * 30
        self._assert_user_is_valid()

    def test_username_cannot_be_over_30_characters_long(self):
        self.user.username = 'x' * 31
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        second_user = User.objects.get(username='janedoe')
        self.user.username = second_user.username
        self._assert_user_is_invalid()

    def test_username_has_numbers(self):
        self.user.username='j0hnd03'
        self._assert_user_is_valid()

# First name tests
    def test_first_name_is_not_blank(self):
        self.user.first_name=''
        self._assert_user_is_invalid()

    def test_first_name_is_not_unique(self):
        second_user = User.objects.get(username='janedoe')
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid()

    def test_first_name_can_have_less_than_50_characters(self):
        self.user.first_name='x' * 50
        self._assert_user_is_valid()

    def test_first_name_cannot_have_more_than_50_characters(self):
        self.user.first_name='x' * 51
        self._assert_user_is_invalid()

# Last name test
    def test_last_name_is_not_blank(self):
        self.user.last_name=''
        self._assert_user_is_invalid()

    def test_last_name_is_not_unique(self):
        second_user = User.objects.get(username='janedoe')
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid()

    def test_last_name_can_have_less_than_50_characters(self):
        self.user.last_name='x' * 50
        self._assert_user_is_valid()

    def test_last_name_cannot_have_more_than_50_characters(self):
        self.user.last_name='x' * 51
        self._assert_user_is_invalid()

# Email tests
    def test_email_is_not_blank(self):
        self.user.email=''
        self._assert_user_is_invalid()

    def test_email_has_to_contain_username(self):
        self.user.email='@example.org'
        self._assert_user_is_invalid()

    def test_email_contains_at(self):
        self.user.email='johndoe.example.org'
        self._assert_user_is_invalid()

    def test_email_contains_domain(self):
        self.user.email='johndoe@'
        self._assert_user_is_invalid()

    def test_email_contains_domain_name(self):
        self.user.email='johndoe@.org'
        self._assert_user_is_invalid()

    def test_email_contains_domain_suffix(self):
        self.user.email='johndoe@example'
        self._assert_user_is_invalid()

    def test_email_is_unique(self):
        second_user = User.objects.get(username='janedoe')
        self.user.email = second_user.email
        self._assert_user_is_invalid()

    def test_email_has_one_at(self):
        self.user.email = 'example@example.org'
        self._assert_user_is_valid()

    def test_email_cannot_have_more_than_one_at(self):
        self.user.email = 'janedoe@@example.org'
        self._assert_user_is_invalid()

# Bio test cases
    def test_bio_can_be_blank(self):
        self.user.bio=''
        self._assert_user_is_valid()

    def test_bio_may_not_be_unique(self):
        second_user = User.objects.get(username='janedoe')
        self.user.bio = second_user.bio
        self._assert_user_is_valid()

    def test_bio_may_have_500_chars(self):
        self.user.bio='x' * 500
        self._assert_user_is_valid()

    def test_bio_cannot_have_over_500_chars(self):
        self.user.bio='x' * 501
        self._assert_user_is_invalid()

# Test case assertions
    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()