from django.core.management.base import BaseCommand, CommandError
from clubs.models import User, Club
from django.contrib.auth.hashers import make_password
from faker import Faker

class Command(BaseCommand):
    """The database seeder."""

    PASSWORD = make_password("Password123", hasher = 'default')

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        print("Starting seed...")

        Command.generate_users(self)

        Command.generate_clubs(self)

        print("Seeding successful!")

    
    # Generate 100 fake users.
    def generate_users(self):
        print("Generating 100 fake users...")
        for i in range(0, 100):
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

    
    # Generate 10 fake clubs.
    def generate_clubs(self):
        print("Generating 10 fake book clubs...")
        for i in range(0, 10):
            fakeName = self.faker.company()
            fakeDescription = self.faker.text(max_nb_chars = 500)

            Club.objects.create(
                name = fakeName,
                description = fakeDescription
            )
        print("Done!")