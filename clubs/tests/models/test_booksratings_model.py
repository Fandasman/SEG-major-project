from django.test import TestCase
from django.core.exceptions import ValidationError
from clubs.models import User, Book, BooksRatings

class BooksRatingsModelTestCase(TestCase):
    """Unit tests for the booksratings model."""

    fixtures = [
        "clubs/tests/fixtures/default_user.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/default_book.json",
        "clubs/tests/fixtures/other_books.json"
    ]

    def setUp(self):
        self.book = Book.objects.get(id = 1)
        self.user = User.objects.get(username = 'johndoe')
        self.rating = BooksRatings.objects.create(
            isbn = self.book.isbn,
            rating = 3,
            user = self.user
        )

    # ISBN tests
    def test_isbn_is_not_blank(self):
        self.rating.isbn=''
        self._assert_rating_is_invalid()

    def test_isbn_can_have_less_than_13_characters(self):
        self.rating.isbn='x' * 13
        self._assert_rating_is_valid()

    def test_isbn_cannot_have_more_than_13_characters(self):
        self.rating.isbn='x' * 14
        self._assert_rating_is_invalid()

    def test_isbn_does_not_have_to_be_unique(self):
        second_rating = self._get_second_rating()
        
        self.rating.isbn = second_rating.isbn
        self._assert_rating_is_valid()

    # User tests
    def test_user_is_not_blank(self):
        self.rating.user=None
        self._assert_rating_is_invalid()

    def test_rating_is_deleted_upon_deleting_the_user_model(self):
        self.user.delete()
        with self.assertRaises(BooksRatings.DoesNotExist):
            BooksRatings.objects.get(pk = self.rating.pk)
        self._assert_rating_is_invalid()

    def test_user_does_not_have_to_be_unique(self):
        second_rating = self._get_second_rating()
        self.rating.user = second_rating.user
        self._assert_rating_is_valid()

    # Rating tests
    def test_rating_is_not_blank(self):
        self.rating.rating = ''
        self._assert_rating_is_invalid()

    def test_rating_can_be_up_to_5(self):
        self.rating.rating = 5
        self._assert_rating_is_valid()

    def test_rating_cannot_be_over_5(self):
        self.rating.rating = 6
        self._assert_rating_is_invalid()

    def test_rating_can_be_1(self):
        self.rating.rating = 1
        self._assert_rating_is_valid()

    def test_rating_cannot_be_under_1(self):
        self.rating.rating = 0
        self._assert_rating_is_invalid()

    def test_rating_does_not_have_to_be_unique(self):
        second_rating = self._get_second_rating()
        self.rating.rating = second_rating.rating
        self._assert_rating_is_valid()

    # Test rating must be a unique together entry.
    def test_rating_must_be_unique_together(self):
        second_rating = self._get_second_rating()
        self.rating.user = second_rating.user
        self.rating.isbn = second_rating.isbn
        self._assert_rating_is_invalid()

    
    # Test case assertions
    def _assert_rating_is_valid(self):
        try:
            self.rating.full_clean()
        except (ValidationError):
            self.fail('Test should be valid')

    def _assert_rating_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.rating.full_clean()

    # Create second rating
    def _get_second_rating(self):
        second_book=Book.objects.get(title="The Transformation")
        second_rating = BooksRatings.objects.create(
            isbn = second_book.isbn,
            rating = 3,
            user = User.objects.get(username = 'janedoe')
        )
        return second_rating