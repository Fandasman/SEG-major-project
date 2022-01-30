from django.core.management.base import BaseCommand, CommandError
from clubs.models import User
from django.contrib.auth.hashers import make_password
from faker import Faker

class Command(BaseCommand):
    """The database seeder."""

    PASSWORD = make_password("Password123", hasher = 'default')

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        print("Generating 100 fake users...")

        for i in range(1, 101):
            fakeUsername = self.faker.user_name() + str(i)
            fakeFirstName = self.faker.first_name()
            fakeLastName = self.faker.last_name()
            fakeEmail = fakeUsername + "@example.org"
            fakeBio = self.faker.text(max_nb_chars = 500)

            User.objects.create(
                username = fakeUsername,
                first_name = fakeFirstName,
                last_name = fakeLastName,
                email = fakeEmail,
                password = Command.PASSWORD,
                bio = fakeBio
            )
        
        print("Done!")