from django.test import TestCase
from django.core.exceptions import ValidationError
from clubs.models import Book

class BookModelTestCase(TestCase):
    """Unit tests for the book model."""

    fixtures = [
        "clubs/tests/fixtures/default_book.json",
        "clubs/tests/fixtures/other_books.json"
    ]

    def setUp(self):
        self.book = Book.objects.get(title = "Bob in Wonderland")

# ISBN tests
    def test_isbn_is_not_blank(self):
        self.book.isbn=''
        self._assert_book_is_invalid()

    def test_isbn_must_be_unique(self):
        second_book=Book.objects.get(title="The Transformation")
        self.book.isbn=second_book.isbn
        self._assert_book_is_invalid()

    def test_isbn_can_have_less_than_17_characters(self):
        self.book.isbn='x' * 17
        self._assert_book_is_valid()

    def test_isbn_cannot_have_more_than_17_characters(self):
        self.book.isbn='x' * 18
        self._assert_book_is_invalid()

# Title tests
    def test_title_is_not_blank(self):
        self.book.title=''
        self._assert_book_is_invalid()

    def test_title_must_be_unique(self):
        second_book=Book.objects.get(title="The Transformation")
        self.book.title=second_book.title
        self._assert_book_is_invalid()

    def test_title_can_have_less_than_100_characters(self):
        self.book.title='x' * 100
        self._assert_book_is_valid()

    def test_isbn_cannot_have_more_than_100_characters(self):
        self.book.title='x' * 101
        self._assert_book_is_invalid()

# Author tests

# Year published tests

# Test case assertions
    def _assert_book_is_valid(self):
        try:
            self.book.full_clean()
        except (ValidationError):
            self.fail('Test should be valid')

    def _assert_book_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.book.full_clean()