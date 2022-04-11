from django.test import TestCase
from clubs.models import User, Club
from clubs.forms import UserPostForm

class UserPostFormTestCase(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.club = Club.objects.get(id=1)

    def test_valid_post_form(self):
        input = {'text': 'x'*200, 'author':self.user, 'club':self.club}
        form = UserPostForm(data=input)
        self.assertTrue(form.is_valid())

    def test_too_long_comment(self):
        input = {'body': 'x'*281, 'user':self.user, 'club':self.club}
        form = UserPostForm(data=input)
        self.assertFalse(form.is_valid())
