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
        self.club = Club.objects.get(name='Booker')
        self.book = Book.objects.get(title='Bob in Wonderland')
        self.role = Role.objects.create(user=self.user, club=self.club, role="O")
        self.url = reverse('set_club_book', kwargs={"club_id": self.club.id})
        self.form_input = {
            'book_title': 'Bob in Wonderland',
        }

    def test_add_repeat_club_book(self):
        self.role.refresh_from_db()
        self.club._add_book(self.book)
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('set_club_book', kwargs={"club_id": self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    def test_successful_set_club_book_(self):
        self.role.refresh_from_db()
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('club_feed', kwargs={"club_id":self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.club.refresh_from_db()
        self.assertEqual(self.club.club_book, self.book)
