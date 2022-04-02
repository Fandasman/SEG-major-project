from django.test import TestCase
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from clubs.models import User, Book, BooksRatings

class WishViewTestCase(TestCase):

    fixtures = ["clubs/tests/fixtures/default_user.json",
                "clubs/tests/fixtures/default_book.json"]

    def setUp(self):
        self.user = User.objects.get(username = 'johndoe')
        self.book = Book.objects.get(pk=1)
        self.url = reverse('remove_rating', args=(self.book.id,))

        self.rating = BooksRatings.objects.create(
            isbn = self.book.isbn,
            user = self.user,
            rating = 3
        )

    def test_remove_rating_url(self):
        self.assertEqual(self.url, '/remove_rating/1')

    def test_remove_rating_redirects_when_logged_out(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)

    def test_valid_remove_rating(self):
        self.client.login(username=self.user.username, password="Password123")
        before_count = BooksRatings.objects.count()
        remove_rating_url = reverse('remove_rating', args=(self.book.id,))
        response = self.client.get(remove_rating_url, follow = True)
        redirect_url = reverse('show_book', args=(self.book.id,))
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'show_book.html')
        after_count = BooksRatings.objects.count()
        self.assertEqual(after_count, before_count - 1)

    def test_remove_book_rating_twice(self):
        self.client.login(username=self.user.username, password="Password123")
        before_count = BooksRatings.objects.count()
        url = reverse('remove_rating', args=(self.book.id,))
        self.client.get(url)
        response = self.client.get(url, follow = True)
        redirect_url = reverse('show_book', args=(self.book.id,))
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'show_book.html')
        after_count = BooksRatings.objects.count()
        self.assertEqual(after_count, before_count - 1)

    def test_remove_invalid_book_rating(self):
        self.client.login(username=self.user.username, password="Password123")
        url = reverse('remove_rating', args=(self.book.id + 9999999,))
        response = self.client.get(url, follow = True)
        redirect_url = reverse('search_books')
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'search_books.html')
        self.assertEqual(BooksRatings.objects.count(), 1)