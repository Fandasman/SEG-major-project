from django.test import TestCase
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from clubs.models import Club, User, Role, Book, Event


class LeaveClubTestCase(TestCase):


    fixtures = ['clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_applicant.json',
                'clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_applicants.json',
                'clubs/tests/fixtures/default_book.json',
                'clubs/tests/fixtures/default_event.json'
                ]

    def setUp(self):
        self.user = User.objects.get(username = "johndoe")
        self.club = Club.objects.get(name ="Booker")
        self.url = reverse('leave_club',kwargs ={'club_id': self.club.id})

    def test_user_leaves_club_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)

    def test_user_leaves_club(self):
        self.client.login(username = self.user.username, password='Password123')
        before_count = Role.objects.filter(club = self.club).count()
        response = self.client.post(self.url, follow = True)
        after_count = Role.objects.filter(club = self.club).count()
        self.assertEqual(after_count, before_count - 1)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    def test_owner_cannot_leave_club(self):
        role = Role.objects.filter(club = self.club).get(user = self.user)
        role.role = "CO"
        role.save()
        self.client.login(username = self.user.username, password='Password123')
        before_count = Role.objects.filter(club = self.club).count()
        response = self.client.post(self.url, follow = True)
        after_count = Role.objects.filter(club = self.club).count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
