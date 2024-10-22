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
        self.url = reverse('unwish', args=(self.book.id,))
        self.user.wishlist.add(self.book)

    def test_unwish_url(self):
        self.assertEqual(self.url, '/book/1/unwish')

    def test_unwish_redirects_when_logged_out(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)

    def test_valid_remove_book_from_wishlist(self):
        self.client.login(username=self.user.username, password="Password123")
        before_count = self.user.wishlist.count()
        unwish_url = reverse('unwish', args=(self.book.id,))
        response = self.client.get(unwish_url, follow = True)
        redirect_url = reverse('show_book', args=(self.book.id,))
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'book_templates/show_book.html')
        after_count = self.user.wishlist.count()
        self.assertEqual(after_count, before_count - 1)

    def test_remove_book_from_wishlist_twice(self):
        self.client.login(username=self.user.username, password="Password123")
        before_count = self.user.wishlist.count()
        url = reverse('unwish', args=(self.book.id,))
        self.client.get(url)
        response = self.client.get(url, follow = True)
        redirect_url = reverse('show_book', args=(self.book.id,))
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'book_templates/show_book.html')
        after_count = self.user.wishlist.count()
        self.assertEqual(after_count, before_count - 1)

    def test_remove_invalid_book_from_wishlist(self):
        self.client.login(username=self.user.username, password="Password123")
        url = reverse('unwish', args=(self.book.id + 9999999,))
        response = self.client.get(url, follow = True)
        redirect_url = reverse('book_list')
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'book_templates/book_list.html')
        self.assertEqual(self.user.wishlist.count(), 1)

    
