from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Comment,UserPost, User

class CommentTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_post.json'
                ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(username='johndoe')
        self.post = UserPost.objects.get(id=1)
        self.comment = Comment(
            post = self.post,
            club = self.post.club,
            user = self.user,
            body="The quick brown fox jumps over the lazy dog."
        )

    def test_valid_message(self):
        try:
            self.comment.full_clean()
        except ValidationError:
            self.fail("Test message should be valid")

    def test_author_must_not_be_blank(self):
        self.comment.user = None
        with self.assertRaises(ValidationError):
            self.comment.full_clean()

    def test_text_must_not_be_blank(self):
        self.comment.body = ''
        with self.assertRaises(ValidationError):
            self.comment.full_clean()

    def test_text_must_not_be_overlong(self):
        self.comment.body = 'x' * 101
        with self.assertRaises(ValidationError):
            self.comment.full_clean()

    def test_club_must_not_be_blank(self):
        self.comment.club = None
        with self.assertRaises(ValidationError):
            self.comment.full_clean()

    def test_post_must_not_be_blank(self):
        self.comment.post = None
        with self.assertRaises(ValidationError):
            self.comment.full_clean()
