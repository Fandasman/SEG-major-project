from django.test import TestCase
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from clubs.models import User


class WishViewTestCase(TestCase):

    fixtures = ["clubs/tests/fixtures/default_user.json",
                'clubs/tests/fixtures/default_book.json',
                'clubs/tests/fixtures/default_club.json'
                ]

    def setUp(self):
        self.user = User.objects.get(username = 'johndoe')
        self.url = reverse('search_view')

    def test_wish_url(self):
        self.assertEqual(self.url, '/search_view/')

    def test_wish_redirects_when_logged_out(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)

    def test_search_with_book_filter(self):
        search_filter = { 'search' : 'Bob',
                          'filter_field' : 'books'
        }
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, search_filter)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bob in Wonderland')


    def test_search_with_user_filter(self):
        search_filter = { 'search' : 'john',
                          'filter_field' : 'users'
        }
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, search_filter)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'johndoe')


    def test_search_with_club_filter(self):
        search_filter = { 'search' : 'Book',
                          'filter_field' : 'clubs'
        }
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, search_filter)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Booker')

    def test_search_with_all_filter(self):
        User.objects.create_user(username = 'booker',
                email='booker@test.org',
                password='Password123',
                first_name='Book',
                last_name='Er',
                bio='Bookers bio',
            )

        search_filter = { 'search' : 'booker',
                          'filter_field' : 'all'
        }
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, search_filter)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2 results for")
