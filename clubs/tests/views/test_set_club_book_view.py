from django.test import TestCase
from django.urls import reverse
from clubs.models import Club, User, Role, Book


class SetClubBookViewTestCase(TestCase):
    fixtures = [
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/default_book.json',
        'clubs/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username="johndoe")
        self.url = reverse('set_club_book')
        self.club = Club.objects.get(name='Booker')
        self.book = Book.objects.get(title='Bob in Wonderland')
        self.role = Role.objects.create(user=self.user, club=self.club, role="O")
        self.form_input = {
            'book_title': 'Bob in Wonderland',
            'club_name': 'Booker',
        }


    def test_successful_club_book_update(self):
        self.role.refresh_from_db()
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('login')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.club.refresh_from_db()
        self.assertEqual(self.club.club_book, self.book)
