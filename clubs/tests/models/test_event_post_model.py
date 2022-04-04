from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import EventPost,Event, User

class EventPostTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_book.json',
                'clubs/tests/fixtures/default_event.json',]

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(username='johndoe')
        self.post = EventPost(
            user=self.user,
            event=Event.objects.get(id=1)
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

    def test_event_must_not_be_blank(self):
        self.post.event = None
        with self.assertRaises(ValidationError):
            self.post.full_clean()
