from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import UserPost,User,Club,Comment

class UserPostTestCase(TestCase):


        fixtures = ['clubs/tests/fixtures/default_user.json',
                    'clubs/tests/fixtures/default_club.json',
                    'clubs/tests/fixtures/other_users.json',
                    'clubs/tests/fixtures/default_user_post.json',
                    ]

        def setUp(self):
            self.user = User.objects.get(username = "johndoe")
            self.club = Club.objects.get(name = "Booker")
            self.post = UserPost.objects.get(author = self.user, club = self.club)


#Test author field model

        def test_author_field_must_not_be_blank(self):
            self.post.author.delete()
            self._assert_user_post_is_invalid()

        def test_author_field_must_contain_a_user(self):
            self.post.author = self.user
            self._assert_user_post_is_valid()

#Test text field

        def test_text_field_cannot_have_more_than_280_charachters(self):
            self.post.text = "x" * 281
            self._assert_user_post_is_invalid()

        def test_text_field_can_have_280_characthers(self):
            self.post.text = "x" * 280
            self._assert_user_post_is_valid()

        def test_text_field_cannot_be_blank(self):
            self.post.text =''
            self._assert_user_post_is_invalid()

        def test_text_field_can_have_less_than_280_charachters(self):
            self.post.text = "x" * 278
            self._assert_user_post_is_valid()


#Test club field

        def test_club_field_must_not_be_blank(self):
           self.post.club.delete()
           self._assert_user_post_is_invalid()

        def test_author_field_must_contain_a_user(self):
           self.post.club = self.club
           self._assert_user_post_is_valid()


#Test likes field

        def test_like_field_can_be_blank(self):
            self.post.likes.set([])
            self._assert_user_post_is_valid()


#Test has liked

        def test_has_liked_is_true(self):
            self.assertTrue(self.post.has_liked(User.objects.get(username = "alicesmith")))

        def test_has_like_is_false(self):
            self.assertFalse(self.post.has_liked(self.user))



        def _assert_user_post_is_valid(self):
           try:
               self.post.full_clean()
           except (ValidationError):
               self.fail('Test should be valid')

        def _assert_user_post_is_invalid(self):
            with self.assertRaises(ValidationError):
                self.post.full_clean()
