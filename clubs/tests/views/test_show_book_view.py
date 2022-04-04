from django.test import TestCase
from django.urls import reverse
from clubs.forms import RatingForm
from clubs.models import BooksRatings, User, Book
from clubs.tests.helpers import reverse_with_next, LogInTester

class ShowBookTest(TestCase,LogInTester):
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_book.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.org')
        self.target_book = Book.objects.get(isbn='9783161484100')
        self.form_input = {
            'rating': 5,
        }
        self.updated_form_input = {
            'rating': 3,
        }
        self.url = reverse('show_book', kwargs={'book_id': self.target_book.id})

    def test_show_book_url(self):
        self.assertEqual(self.url,f'/book/{self.target_book.id}')

    def test_show_book_redirects_when_logged_out(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)

    def test_get_show_book_with_valid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_templates/show_book.html')
        self.assertContains(response, self.target_book.title)
        self.assertContains(response, self.target_book.author)
        self.assertContains(response, self.target_book.imgURLMedium)
        form = response.context['form']
        self.assertTrue(isinstance(form, RatingForm))

    def test_show_book_with_invalid_id(self):
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('show_book', kwargs={'book_id': 99999999999999})
        response = self.client.get(self.url,follow=True)
        redirect_url = reverse('book_list')
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_unsuccesful_rating(self):
        self.client.login(username=self.user.username, password="Password123")
        self.form_input['rating'] = 0
        before_count = BooksRatings.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = BooksRatings.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(isinstance(form, RatingForm))

    def test_add_new_rating(self):
        self.client.login(username=self.user.username, password="Password123")
        before_count = BooksRatings.objects.count()
        response = self.client.post(self.url, self.form_input, follow = True)
        after_count = BooksRatings.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_templates/show_book.html')
        rating = BooksRatings.objects.get(user = self.user, isbn = self.target_book.isbn)
        self.assertEqual(rating.rating, 5)

    def test_edit_past_rating(self):
        self.client.login(username=self.user.username, password="Password123")
        before_count = BooksRatings.objects.count()
        response = self.client.post(self.url, self.form_input, follow = True)
        after_count = BooksRatings.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_templates/show_book.html')
        rating = BooksRatings.objects.get(user = self.user, isbn = self.target_book.isbn)
        self.assertEqual(rating.rating, 5)
        final_count = BooksRatings.objects.count()
        response = self.client.post(self.url, self.updated_form_input, follow = True)
        self.assertEqual(final_count, after_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_templates/show_book.html')
        rating = BooksRatings.objects.get(user = self.user, isbn = self.target_book.isbn)
        self.assertEqual(rating.rating, 3)
