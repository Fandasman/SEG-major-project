from django.test import TestCase
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from clubs.models import User, Club, Role
from django.core.exceptions import ObjectDoesNotExist

class WishlistViewTestCase(TestCase):

    fixtures = ["clubs/tests/fixtures/default_user.json",
                "clubs/tests/fixtures/other_users.json",
                "clubs/tests/fixtures/default_club.json",]

    def setUp(self):
        self.user = User.objects.get(username = "johndoe")
        self.club = Club.objects.get(id = 1)
        self.role = Role.objects.create(
            user = self.user,
            club = self.club,
            role = "CO"
        )
        self.url = reverse("delete_club_action", args=(self.club.id,))

    def test_delete_club_action_url(self):
        self.assertEquals(self.url, "/club/1/delete/")

    def test_delete_club_action_redirects_when_logged_out(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)

    def test_get_delete_club_action_when_logged_in_as_owner(self):
        self.client.login(username=self.user.username, password="Password123")
        before_count = Club.objects.count()
        response = self.client.get(self.url)
        redirect_url = reverse('feed')
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count - 1)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)

    def test_get_delete_club_action_with_invalid_club_id_redirects_to_feed(self):
        with self.assertRaises(ObjectDoesNotExist):
            self.url = reverse("delete_club_action", args=(99999999999999999,))
            self.client.login(username=self.user.username, password="Password123")
            before_count = Club.objects.count()
            response = self.client.get(self.url)
            redirect_url = reverse('feed')
            after_count = Club.objects.count()
            self.assertEqual(after_count, before_count)
            self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)

    def test_get_delete_club_action_by_member(self):
        second_user = User.objects.get(id = 2)
        self.client.login(username=second_user.username, password="Password123")
        second_role = self._get_second_role
        before_count = Club.objects.count()
        response = self.client.get(self.url)
        redirect_url = reverse('feed')
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)

    def test_get_delete_club_action_by_officer(self):
        second_user = User.objects.get(id = 2)
        self.client.login(username=second_user.username, password="Password123")
        second_role = self._get_second_role()
        second_role.role = "O"
        before_count = Club.objects.count()
        response = self.client.get(self.url)
        redirect_url = reverse('feed')
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)


    # Create second role
    def _get_second_role(self):
        second_user = User.objects.get(id = 2)
        second_club = Club.objects.get(id = 1)
        second_role = Role.objects.create(
            user = second_user,
            club = second_club,
            role = "M"
        )
        return second_role
