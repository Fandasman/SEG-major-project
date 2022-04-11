from django.test import TestCase
from django.urls import reverse
from clubs.models import UserPost, User, Club, Comment
from clubs.tests.helpers import reverse_with_next

class NewCommentTest(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/default_post.json',
        'clubs/tests/fixtures/default_member.json'

    ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(username='johndoe')
        self.club = Club.objects.get(id=1)
        self.post = UserPost.objects.get(id=1)
        self.url = reverse('add_comment', kwargs={'club_id': self.club.id, 'post_id': self.post.id})
        self.data = { 'body': 'The quick brown fox jumps over the lazy dog.'
}

    def test_new_post_(self):
        self.assertEqual(self.url,f'/add_comment/{self.club.id}/{self.post.id}')

    def test_post_new_post_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)


    def test_successful_new_post(self):
        self.client.login(username=self.user.username, password="Password123")
        user_count_before = Comment.objects.count()
        response = self.client.post(self.url, self.data, follow=True)
        user_count_after = Comment.objects.count()
        self.assertEqual(user_count_after, user_count_before+1)
        new_post = Comment.objects.latest('created_at')
        self.assertEqual(self.user, new_post.user)
        response_url = reverse('club_feed', kwargs={'club_id': self.club.id})
        self.assertRedirects(
            response, response_url,
            status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'club_templates/club_feed.html')

    def test_unsuccessful_new_post(self):
        self.client.login(username='johndoe', password='Password123')
        self.data['body'] = ''
        response = self.client.post(self.url, self.data, follow=True)
        self.assertTemplateUsed(response, 'club_templates/club_feed.html')


    def test_cannot_create_post_for_other_user(self):
        self.client.login(username='johndoe', password='Password123')
        other_user = User.objects.get(username='janedoe')
        self.data['user'] = other_user.id
        user_count_before = Comment.objects.count()
        response = self.client.post(self.url, self.data, follow=True)
        user_count_after = Comment.objects.count()
        self.assertEqual(user_count_after, user_count_before+1)
        new_post = Comment.objects.latest('created_at')
        self.assertEqual(self.user, new_post.user)
