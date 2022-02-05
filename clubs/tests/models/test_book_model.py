from django.test import TestCase
import datetime
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

    def test_isbn_can_have_less_than_13_characters(self):
        self.book.isbn='x' * 13
        self._assert_book_is_valid()

    def test_isbn_cannot_have_more_than_13_characters(self):
        self.book.isbn='x' * 14
        self._assert_book_is_invalid()

# Title tests
    def test_title_is_not_blank(self):
        self.book.title=''
        self._assert_book_is_invalid()

    def test_title_does_not_have_to_be_unique(self):
        second_book=Book.objects.get(title="The Transformation")
        self.book.title=second_book.title
        self._assert_book_is_valid()

    def test_title_can_have_less_than_100_characters(self):
        self.book.title='x' * 100
        self._assert_book_is_valid()

    def test_title_cannot_have_more_than_100_characters(self):
        self.book.title='x' * 101
        self._assert_book_is_invalid()

# Author tests
    def test_author_is_not_blank(self):
        self.book.author=''
        self._assert_book_is_invalid()

    def test_author_does_not_need_to_be_unique(self):
        second_book=Book.objects.get(title="The Transformation")
        self.book.author=second_book.author
        self._assert_book_is_valid()

    def test_author_can_have_less_than_100_characters(self):
        self.book.author='x' * 100
        self._assert_book_is_valid()

    def test_author_cannot_have_more_than_100_characters(self):
        self.book.author='x' * 101
        self._assert_book_is_invalid()

# Publisher tests
    def test_publisher_cannot_be_blank(self):
        self.book.publisher=''
        self._assert_book_is_invalid()

    def test_publisher_does_not_need_to_be_unique(self):
        second_book=Book.objects.get(title="The Transformation")
        self.book.publisher=second_book.publisher
        self._assert_book_is_valid()

    def test_publisher_can_have_less_than_100_characters(self):
        self.book.publisher='x' * 100
        self._assert_book_is_valid()

    def test_publisher_cannot_have_more_than_100_characters(self):
        self.book.publisher='x' * 101
        self._assert_book_is_invalid()

# Published tests
    def test_published_can_be_positive(self):
        self.book.published = 1978
        self._assert_book_is_valid()
    
    def test_published_cannot_be_negative(self):
        self.book.published = -1978
        self._assert_book_is_invalid()

    def test_published_can_be_current_year(self):
        currentYear = datetime.datetime.now().year
        self.book.published = currentYear
        self._assert_book_is_valid()
    
    def test_published_cannot_be_larger_than_current_year(self):
        currentYear = datetime.datetime.now().year
        self.book.published = currentYear + 1
        self._assert_book_is_invalid()

# IMGURL tests
    """Blank tests"""
    def test_imgURLSmall_can_be_blank(self):
        self.book.imgURLSmall=''
        self._assert_book_is_valid()
    
    def test_imgURLMedium_can_be_blank(self):
        self.book.imgURLMedium=''
        self._assert_book_is_valid()
    
    def test_imgURLLarge_can_be_blank(self):
        self.book.imgURLLarge=''
        self._assert_book_is_valid()

    """Unique tests"""
    def test_imgURLSmall_does_not_need_to_be_unique(self):
        second_book=Book.objects.get(title="The Transformation")
        self.book.imgURLSmall=second_book.imgURLSmall
        self._assert_book_is_valid()
    
    def test_imgURLMedium_does_not_need_to_be_unique(self):
        second_book=Book.objects.get(title="The Transformation")
        self.book.imgURLMedium=second_book.imgURLMedium
        self._assert_book_is_valid()

    def test_imgURLLarge_does_not_need_to_be_unique(self):
        second_book=Book.objects.get(title="The Transformation")
        self.book.imgURLLarge=second_book.imgURLLarge
        self._assert_book_is_valid()

# Test case assertions
    def _assert_book_is_valid(self):
        try:
            self.book.full_clean()
        except (ValidationError):
            self.fail('Test should be valid')

    def _assert_book_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.book.full_clean()