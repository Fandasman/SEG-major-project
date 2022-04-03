from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, User, MembershipPost

class MembershipTestCase(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_membership_post.json'
                ]

    def setUp(self):
        self.user = User.objects.get(username = "johndoe")
        self.club = Club.objects.get(name = "Booker")
        self.membership_post = MembershipPost.objects.get(user = self.user, club = self.club)


# Test user field

    def test_user_field_cannot_be_blank(self):
        self.membership_post.user.delete()
        self._assert_membership_post_is_invalid()

    def test_user_field_must_must_have_a_user(self):
        self.membership_post.user = self.user
        self._assert_membership_post_is_valid()

# Test club field

    def test_club_field_must_not_be_blank(self):
        self.membership_post.club.delete()
        self._assert_membership_post_is_invalid()

    def test_club_field_must_must_have_a_user(self):
        self.membership_post.club= self.club
        self._assert_membership_post_is_valid()


#Test join field
    def test_default_value_for_join_is_true(self):
        self.assertTrue(self.membership_post.join)

#Test description function

    def test_output_of_description_functio_if_join_is_true(self):
        self.assertEqual("has joined this club",self.membership_post.description())


    def test_output_of_description_functio_if_join_is_false(self):
        self.membership_post.join = False
        self.assertEqual("has left this club",self.membership_post.description())



    def _assert_membership_post_is_valid(self):
       try:
           self.membership_post.full_clean()
       except (ValidationError):
           self.fail('Test should be valid')

    def _assert_membership_post_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.membership_post.full_clean()
