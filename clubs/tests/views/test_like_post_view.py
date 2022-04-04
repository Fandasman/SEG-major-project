from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club, UserPost
from clubs.tests.helpers import reverse_with_next

class LikeToggleTest(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/default_member.json',
        'clubs/tests/fixtures/default_post.json'

    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.club = Club.objects.get(id=1)
        self.post = UserPost.objects.get(id=1)
        self.url = reverse('like_post', kwargs={'club_id': self.club.id, 'post_id': self.post.id})

    def test_follow_toggle_url(self):
        self.assertEqual(self.url,f'/like_post/{self.club.id}/{self.post.id}')

    def test_get_follow_toggle_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_like_toggle_for_liked_post(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        likes_before = self.post.number_of_likes()
        self.assertTrue(self.post.likes.filter(id=self.user.id).exists())
        response = self.client.get(self.url, follow=True)
        likes_after = self.post.number_of_likes()
        self.assertEqual(likes_before, likes_after+1)
        self.assertFalse(self.post.likes.filter(id=self.user.id).exists())
        response_url = reverse('club_feed', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_templates/club_feed.html')

    def test_get_like_toggle_for_unliked_post(self):
        self.client.login(username=self.user.username, password='Password123')
        likes_before = self.post.number_of_likes()
        self.assertFalse(self.post.likes.filter(id=self.user.id).exists())
        response = self.client.get(self.url, follow=True)
        likes_after = self.post.number_of_likes()
        self.assertEqual(likes_before+1, likes_after)
        self.assertTrue(self.post.likes.filter(id=self.user.id).exists())
        response_url = reverse('club_feed', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_templates/club_feed.html')

    def test_like_toggle_with_invalid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('like_post', kwargs={'club_id': self.club.id, 'post_id': self.post.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('club_feed', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_templates/club_feed.html')
