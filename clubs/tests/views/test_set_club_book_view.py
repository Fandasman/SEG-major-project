from django.test import TestCase
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from clubs.models import Club, User, Role, Book


class SetClubBookViewTestCase(TestCase):
    fixtures = [
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/default_book.json',
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.other_user = User.objects.get(username='janedoe')
        self.club = Club.objects.get(name='Booker')
        self.book = Book.objects.get(title='Bob in Wonderland')
        self.role = Role.objects.create(user=self.user, club=self.club, role="O")
        self.url = reverse('set_club_book', kwargs={"club_id": self.club.id})
        self.form_input = {
            'book_title': 'Bob in Wonderland',
        }

    def test_set_club_view_redirects_when_logged_out(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)

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

    def test_unsuccessful_set_book_without_permission(self):
        self.client.login(username=self.other_user.username, password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('club_list')
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), "you don't own this club")
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    def test_unsuccessful_set_book_with_invalid_username(self):
        self.form_input = {
            'book_title': 'x',
        }
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('set_club_book', kwargs={'club_id': self.club.id})
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'Invalid club name or book name')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)