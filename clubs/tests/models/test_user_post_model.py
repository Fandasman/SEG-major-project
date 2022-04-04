from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import UserPost, User, Club

class UserPostTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_post.json'
                ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.post = UserPost.objects.get(id=1)

    def test_valid_message(self):
        try:
            self.post.full_clean()
        except ValidationError:
            self.fail("Test message should be valid")

    def test_author_must_not_be_blank(self):
        self.post.author = None
        with self.assertRaises(ValidationError):
            self.post.full_clean()

    def test_text_must_not_be_blank(self):
        self.post.text = ''
        with self.assertRaises(ValidationError):
            self.post.full_clean()

    def test_club_must_not_be_blank(self):
        self.post.club = None
        with self.assertRaises(ValidationError):
            self.post.full_clean()

    def test_like_counters(self):
        bob = User.objects.get(username='bobsmith')
        jane = User.objects.get(username='janedoe')
        alice = User.objects.get(username='alicesmith')
        self.post.likes.add(bob)
        self.post.likes.add(alice)
        self.post.likes.add(jane)
        self.assertEqual(self.post.number_of_likes(), 3)

    def test_has_liked(self):
        bob = User.objects.get(username='bobsmith')
        self.assertFalse(self.post.has_liked(bob))
        self.post.likes.add(bob)
        self.assertTrue(self.post.has_liked(bob))
