from django.test import TestCase
from django.urls import reverse
from clubs.models import UserPost, User, Club

class NewPostTest(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/default_member.json'

    ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(username='johndoe')
        self.club = Club.objects.get(id=1)
        self.url = reverse('new_post', kwargs={'club_id': self.club.id})
        self.data = { 'text': 'The quick brown fox jumps over the lazy dog.' }

    def test_new_post_url(self):
        self.assertEqual(self.url,f'/new_post/{self.club.id}/')

    def test_get_new_post_is_forbidden(self):
        self.client.login(username=self.user.username, password="Password123")
        post_count_before = UserPost.objects.count()
        response = self.client.get(self.url, follow=True)
        post_count_after = UserPost.objects.count()
        self.assertEqual(post_count_after, post_count_before)
        self.assertEqual(response.status_code, 405)

    def test_post_new_post_redirects_when_not_logged_in(self):
        user_count_before = UserPost.objects.count()
        redirect_url = reverse('login')
        response = self.client.post(self.url, self.data, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        user_count_after = UserPost.objects.count()
        self.assertEqual(user_count_after, user_count_before)

    def test_successful_new_post(self):
        self.client.login(username=self.user.username, password="Password123")
        user_count_before = UserPost.objects.count()
        response = self.client.post(self.url, self.data, follow=True)
        user_count_after = UserPost.objects.count()
        self.assertEqual(user_count_after, user_count_before+1)
        new_post = UserPost.objects.latest('created_at')
        self.assertEqual(self.user, new_post.author)
        response_url = reverse('club_feed', kwargs={'club_id': self.club.id})
        self.assertRedirects(
            response, response_url,
            status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'club_templates/club_feed.html')

    # def test_unsuccessful_new_post(self):
    #     self.client.login(username=self.user.username, password='Password123')
    #     user_count_before = UserPost.objects.count()
    #     self.data['text'] = 'h'*289
    #     response = self.client.post(self.url, self.data, follow=True)
    #     user_count_after = UserPost.objects.count()
    #     self.assertEqual(user_count_after, user_count_before)
    #     self.assertTemplateUsed(response, 'club_templates/club_feed.html')


    def test_cannot_create_post_for_other_user(self):
        self.client.login(username='johndoe', password='Password123')
        other_user = User.objects.get(username='janedoe')
        self.data['user'] = other_user.id
        user_count_before = UserPost.objects.count()
        response = self.client.post(self.url, self.data, follow=True)
        user_count_after = UserPost.objects.count()
        self.assertEqual(user_count_after, user_count_before+1)
        new_post = UserPost.objects.latest('created_at')
        self.assertEqual(self.user, new_post.author)
