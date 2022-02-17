from django.test import TestCase
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from clubs.models import User, Book

class WishViewTestCase(TestCase):

    fixtures = ["clubs/tests/fixtures/default_user.json",
                "clubs/tests/fixtures/default_book.json"]

    def setUp(self):
        self.user = User.objects.get(username = 'johndoe')
        self.book = Book.objects.get(pk=1)

    def test_wish_url(self):
        url = reverse('wish', args=(self.book.id,))
        self.assertEqual(url, '/book/1/wish')

    def test_valid_add_book_to_wishlist(self):
        self.client.login(username=self.user.username, password="Password123")
        before_count = self.user.wishlist.count()
        url = reverse('wish', args=(self.book.id,))
        self.client.get(url)
        after_count = self.user.wishlist.count()
        self.assertEqual(after_count, before_count + 1)

    def test_add_alredy_wishlisted_book(self):
        self.client.login(username=self.user.username, password="Password123")
        before_count = self.user.wishlist.count()
        url = reverse('wish', args=(self.book.id,))
        self.client.get(url)
        self.client.get(url)
        after_count = self.user.wishlist.count()
        self.assertEqual(after_count, before_count + 1)

    def test_add_nonexisting_book_to_wishlist(self):
        self.client.login(username=self.user.username, password="Password123")
        url = reverse('wish', args=(self.book.id + 9999999,))
        response = self.client.get(url, follow = True)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'feed.html')
        self.assertEqual(self.user.wishlist.count(), 0)