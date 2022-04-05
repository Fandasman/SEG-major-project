from django.test import TestCase
from clubs.models import User, UserPost, Club
from clubs.forms import CommentForm

class CommentPostFormTestCase(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_post.json'
                ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.post = UserPost.objects.get(id=1)
        self.club = self.post.club

    def test_valid_post_form(self):
        input = {'body': 'x'*20, 'user':self.user, 'post':self.post, 'club':self.club}
        form = CommentForm(data=input)
        self.assertTrue(form.is_valid())

    def test_too_long_comment(self):
        input = {'body': 'x'*101, 'user':self.user, 'post':self.post, 'club':self.club}
        form = CommentForm(data=input)
        self.assertFalse(form.is_valid())
