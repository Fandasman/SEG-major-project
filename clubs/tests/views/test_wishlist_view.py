from django.test import TestCase
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from clubs.models import User

class WishlistViewTestCase(TestCase):

    fixtures = ["clubs/tests/fixtures/default_user.json",
                "clubs/tests/fixtures/other_users.json"]

    def setUp(self):
        self.user = User.objects.get(username = "johndoe")
        self.url = reverse("wishlist", args=(self.user.pk,))

    def test_wishlist_url(self):
        self.assertEquals(self.url, "/user/1/wishlist")

    def test_wishlist_redirects_when_logged_out(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)

    def test_get_wishlist_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("wishlist.html")
