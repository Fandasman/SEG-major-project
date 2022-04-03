from django.test import TestCase
from django.core.exceptions import ValidationError
from clubs.models import User, Club, UserPost,Comment

class CommentTestCase(TestCase):
    """Unit tests of the club model."""

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_user_post.json',
                'clubs/tests/fixtures/default_comment.json',
                ]

    def setUp(self):
        self.user = User.objects.get(username = "johndoe")
        self.club = Club.objects.get(name = "Booker")
        self.post = UserPost.objects.get(author = self.user, club = self.club)
        self.comment =Comment.objects.get()

#Test post field
    def test_post_field_must_not_be_blank(self):
       self.comment.post.delete()
       self._assert_comment_is_invalid()

    def test_must_contain_a_post(self):
        self.comment.post = self.post
        self._assert_comment_is_valid()

#Test body field

    def test_body_field_cannot_have_more_than_100_charachters(self):
        self.comment.body = "x" * 101
        self._assert_comment_is_invalid()

    def test_body_can_contain_100_charachters(self):
        self.comment.body = "x" * 100
        self._assert_comment_is_valid()

    def test_body_can_contain_less_than_100_charachters(self):
        self.comment.body = "x" * 99
        self._assert_comment_is_valid()

    def test_body_cannot_be_blank(self):
        self.comment.body =''
        self._assert_comment_is_invalid()

#Test use field

    def test_user_field_cannot_be_blank(self):
        self.comment.user.delete()
        self._assert_comment_is_invalid()

    def test_comment_must_contain_a_user(self):
        self.comment.user = self.user
        self._assert_comment_is_valid()

#Test club field

    def test_club_field_must_not_be_blank(self):
        self.comment.club.delete()
        self._assert_comment_is_invalid()

    def test_comment_must_contain_a_club(self):
        self.comment.club = self.club
        self._assert_comment_is_valid()



    def _assert_comment_is_valid(self):
       try:
           self.comment.full_clean()
       except (ValidationError):
           self.fail('Test should be valid')

    def _assert_comment_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.comment.full_clean()
