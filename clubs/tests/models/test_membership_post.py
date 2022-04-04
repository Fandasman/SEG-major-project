from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import MembershipPost, User, Club

class MembershipPostTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
]
    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(username='johndoe')
        self.club=Club.objects.get(id=1)
        self.post = MembershipPost(
            user=self.user,
            club=self.club,
            join=True
        )

    def test_valid_message(self):
        try:
            self.post.full_clean()
        except ValidationError:
            self.fail("Test message should be valid")

    def test_author_must_not_be_blank(self):
        self.post.user = None
        with self.assertRaises(ValidationError):
            self.post.full_clean()

    def test_join_must_not_be_blank(self):
        self.post.join = None
        with self.assertRaises(ValidationError):
            self.post.full_clean()

    def test_description_correct_output(self):
        self.assertEqual(self.post.description(), 'has joined this club')
        self.post.join = False
        self.assertEqual(self.post.description(), 'has left this club')
