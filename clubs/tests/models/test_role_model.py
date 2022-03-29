from django.test import TestCase
from django.core.exceptions import ValidationError
from clubs.models import User, Club

class RoleModelTestCase(TestCase):
    """Unit tests of the club model."""

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_clubs.json',]

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(username='johndoe')
        self.club = Club.objects.get(name="Booker")
