import csv
from django.core.management.base import BaseCommand, CommandError
from clubs.models import User, Book, Club
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

        Command.get_books(self, **options)

        print("Seeding complete!")

    
    # Generate fake users.
    def generate_users(self):
        print("Generating club owner profile...")
        User.objects.create(
            username = 'charlie',
            first_name = 'Charlie',
            last_name = 'Czechman',
            email = 'charlie@example.org',
            password = Command.PASSWORD,
            bio = 'Hi, I own all the clubs here. Care to join?'
        )
        print("Done!")

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
            fakeLocation = self.faker.address()
            fakeDescription = self.faker.text(max_nb_chars = 500)

            Club.objects.create(
                name = fakeName,
                leader = User.objects.get(username = 'charlie'),
                location = fakeLocation,
                description = fakeDescription
            )
        print("Done!")

    # Read books from BX_Books.csv
    def get_books(self, **options):
        print("Reading books from BX_Books.csv...")
        
        try:
            with open("BX_Books.csv", 'r', encoding = 'latin-1') as csv_file:
                csvreader = csv.reader(csv_file, delimiter = ";")
                header = next(csvreader)

                for row in csvreader:
                    Book.objects.create(
                        isbn = row[0],
                        title = row[1],
                        author = row[2],
                        published = row[3],
                        publisher = row[4],
                        imgURLSmall = row[5],
                        imgURLMedium = row[6],
                        imgURLLarge = row[7]
                    )
        except OSError as e:
            print("File not found. Make sure it's in the right directory!")
            print(e)

        print("Done!")