from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Book
from clubs.tests.helpers import reverse_with_next, LogInTester

class ShowBookTest(TestCase,LogInTester):
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_book.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.org')
        self.target_book = Book.objects.get(isbn='9783161484100')
        self.url = reverse('show_book', kwargs={'book_id': self.target_book.id})

    def test_show_book_url(self):
        self.assertEqual(self.url,f'/book/{self.target_book.id}')

    def test_get_show_book_with_valid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_templates/show_book.html')
        self.assertContains(response, self.target_book.title)
        self.assertContains(response, self.target_book.author)
        self.assertContains(response, self.target_book.imgURLMedium)


    def test_show_book_with_invalid_id(self):
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('show_book', kwargs={'book_id': 99999999999999})
        response = self.client.get(self.url,follow=True)
        redirect_url = reverse('search_books')
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
