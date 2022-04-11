from django.test import TestCase
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from clubs.models import Club, User, Role, Book, Invitation


class InviteViewTestCase(TestCase):
    fixtures = [
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/default_book.json',
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_invitation.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username="johndoe")
        self.other_user = User.objects.get(username="alicesmith")
        self.club = Club.objects.get(name='Booker')
        self.role = Role.objects.create(user=self.user, club=self.club, role="O")
        self.invitation = Invitation.objects.get(id=1)
        self.url = reverse('invite', kwargs={"club_id": self.club.id})
        self.form_input = {
            'username': 'alicesmith',
        }

    def test_template_used_by_invite_view(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_templates/invite.html')


    def test_invite_view_redirects_when_logged_out(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)

    def test_successful_invite_user(self):
        self.role.refresh_from_db()
        self.client.login(username=self.user.username, password="Password123")
        before_count = Invitation.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Invitation.objects.count()
        response_url = reverse('club_members', kwargs={"club_id": self.club.id})
        self.assertEqual(after_count, before_count+1)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)


    def test_successful_accept_invitation(self):
        invitation = Invitation.objects.create(club=self.club, user=self.other_user, status='P')
        url = reverse('accept_invitation', kwargs={"inv_id":invitation.id})
        self.client.login(username=self.other_user.username, password="Password123")
        response_url = reverse('invitation_list', kwargs={"user_id": self.other_user.id})
        before_count = Role.objects.count()
        response = self.client.post(url, follow=True)
        after_count = Role.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        new_role = Role.objects.get(club=self.club, user=self.other_user)
        self.assertEqual(new_role.role, 'M')

    def test_forbidden_get_request_accept_invitation(self):
        self.client.login(username=self.user.username, password="Password123")
        invitation = Invitation.objects.create(club=self.club, user=self.other_user, status='P')
        url = reverse('accept_invitation', kwargs={"inv_id":invitation.id})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_successful_reject_invitation(self):
        invitation = Invitation.objects.create(club=self.club, user=self.other_user, status='P')
        url = reverse('reject_invitation', kwargs={"inv_id": invitation.id})
        self.client.login(username=self.other_user.username, password="Password123")
        response_url = reverse('invitation_list', kwargs={"user_id": self.other_user.id})
        before_count = Invitation.objects.count()
        response = self.client.post(url, follow=True)
        after_count = Invitation.objects.count()
        self.assertEqual(after_count, before_count - 1)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    def test_forbidden_get_request_reject_invitation(self):
        self.client.login(username=self.user.username, password="Password123")
        invitation = Invitation.objects.create(club=self.club, user=self.other_user, status='P')
        url = reverse('reject_invitation', kwargs={"inv_id":invitation.id})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 403)


    def test_unsuccessful_repeat_invite_same_user(self):
        invitation = Invitation.objects.create(club=self.club, user=self.other_user, status='P')
        self.client.login(username=self.user.username, password="Password123")
        before_count = Invitation.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Invitation.objects.count()
        response_url = reverse('invite', kwargs={'club_id': self.club.id})
        messages = list(response.context['messages'])
        self.assertEqual(after_count, before_count)
        self.assertEqual(str(messages[0]), 'you have already invited this user or this user already in the club')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    def test_unsuccessful_invite_user_without_permission(self):
        self.client.login(username=self.other_user.username, password="Password123")
        before_count = Invitation.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Invitation.objects.count()
        response_url = reverse('club_list')
        messages = list(response.context['messages'])
        self.assertEqual(after_count, before_count)
        self.assertEqual(str(messages[0]), "you don't have the permission to invite others")
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    def test_unsuccessful_invite_user_with_invalid_username(self):
        self.form_input = {
            'username': 'x',
        }
        self.client.login(username=self.user.username, password="Password123")
        before_count = Invitation.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Invitation.objects.count()
        response_url = reverse('invite', kwargs={'club_id': self.club.id})
        messages = list(response.context['messages'])
        self.assertEqual(after_count, before_count)
        self.assertEqual(str(messages[0]), 'Invalid username')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
