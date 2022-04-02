from django.test import TestCase
from django.urls import reverse
from microblogs.models import Post, User

class NewPostTest(TestCase):

    fixtures = [
        'microblogs/tests/fixtures/default_user.json',
        'microblogs/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('new_post')
        self.data = { 'text': 'The quick brown fox jumps over the lazy dog.' }

    def test_new_post_url(self):
        self.assertEqual(self.url,'/new_post/')

    def test_get_new_post_is_forbidden(self):
        self.client.login(username=self.user.username, password="Password123")
        user_count_before = Post.objects.count()
        response = self.client.get(self.url, follow=True)
        user_count_after = Post.objects.count()
        self.assertEqual(user_count_after, user_count_before)
        self.assertEqual(response.status_code, 405)

    def test_post_new_post_redirects_when_not_logged_in(self):
        user_count_before = Post.objects.count()
        redirect_url = reverse('log_in')
        response = self.client.post(self.url, self.data, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        user_count_after = Post.objects.count()
        self.assertEqual(user_count_after, user_count_before)

    def test_successful_new_post(self):
        self.client.login(username=self.user.username, password="Password123")
        user_count_before = Post.objects.count()
        response = self.client.post(self.url, self.data, follow=True)
        user_count_after = Post.objects.count()
        self.assertEqual(user_count_after, user_count_before+1)
        new_post = Post.objects.latest('created_at')
        self.assertEqual(self.user, new_post.author)
        response_url = reverse('feed')
        self.assertRedirects(
            response, response_url,
            status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')

    def test_unsuccessful_new_post(self):
        self.client.login(username='@johndoe', password='Password123')
        user_count_before = Post.objects.count()
        self.data['text'] = ""
        response = self.client.post(self.url, self.data, follow=True)
        user_count_after = Post.objects.count()
        self.assertEqual(user_count_after, user_count_before)
        self.assertTemplateUsed(response, 'feed.html')

    def test_cannot_create_post_for_other_user(self):
        self.client.login(username='@johndoe', password='Password123')
        other_user = User.objects.get(username='@janedoe')
        self.data['author'] = other_user.id
        user_count_before = Post.objects.count()
        response = self.client.post(self.url, self.data, follow=True)
        user_count_after = Post.objects.count()
        self.assertEqual(user_count_after, user_count_before+1)
        new_post = Post.objects.latest('created_at')
        self.assertEqual(self.user, new_post.author)
