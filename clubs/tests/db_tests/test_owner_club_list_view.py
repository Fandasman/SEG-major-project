from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from clubs.models import Book, Club, User
from clubs.tests.helpers import reverse_with_next

class OwnerClubListTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_book.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_applicants.json']

    def setUp(self):
        self.url = reverse('owner_club_list')
        self.user = User.objects.get(username='bobsmith')
        self.club = Club.objects.get(name='Booker')
        self.book = Book.objects.get(isbn='9783161484100')

    def test_owner_club_list_url(self):
        self.assertEqual(self.url,'/owner_club_list')

    def test_get_owner_club_list(self):
        self.client.login(username=self.user.username, password='Password123')
        self._create_test_clubs(settings.CLUBS_PER_PAGE-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/owner_club_list.html')
        self.assertEqual(len(response.context['clubs']), settings.CLUBS_PER_PAGE)
        self.assertFalse(response.context['is_paginated'])
        for club_id in range(settings.CLUBS_PER_PAGE-1):
            self.assertContains(response, self.club.name)
            self.assertContains(response, self.club.location)
            club = Club.objects.get(name= self.club.name)
            club_url = reverse('club_feed', kwargs={'club_id': role.club.id})
            self.assertContains(response, club_url)

    def test_get_owner_club_list_with_pagination(self):
        self.client.login(username=self.user.username, password='Password123')
        self._create_test_clubs(settings.CLUBS_PER_PAGE*2+3-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/owner_club_list.html')
        self.assertEqual(len(response.context['clubs']), settings.CLUBS_PER_PAGE)
        self.assertTrue(response.context['is_paginated'])
        page_obj = response.context['page_obj']
        self.assertFalse(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())
        page_one_url = reverse('owner_club_list') + '?page=1'
        response = self.client.get(page_one_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/owner_club_list.html')
        self.assertEqual(len(response.context['clubs']), settings.CLUBS_PER_PAGE)
        page_obj = response.context['page_obj']
        self.assertFalse(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())
        page_two_url = reverse('owner_club_list') + '?page=2'
        response = self.client.get(page_two_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/owner_club_list.html')
        self.assertEqual(len(response.context['clubs']), settings.CLUBS_PER_PAGE)
        page_obj = response.context['page_obj']
        self.assertTrue(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())
        page_three_url = reverse('owner_club_list') + '?page=3'
        response = self.client.get(page_three_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/owner_club_list.html')
        self.assertEqual(len(response.context['clubs']), 3)
        page_obj = response.context['page_obj']
        self.assertTrue(page_obj.has_previous())
        self.assertFalse(page_obj.has_next())

    def test_get_owner_club_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def _create_test_clubs(self, club_count=10):
        for club_id in range(club_count):
            club = Club(
                name = self.club.name,
                location = self.club.location,
                description = self.club.description,
                club_book = self.book,
            )
            club.save()
