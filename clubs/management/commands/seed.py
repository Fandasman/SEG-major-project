import random
import pandas as pd
from tqdm import tqdm
from django.core.management.base import BaseCommand, CommandError
from clubs.models import User, Book, BooksRatings, Club, Role
from django.contrib.auth.hashers import make_password
from faker import Faker

class Command(BaseCommand):
    """The database seeder."""

    PASSWORD = make_password("Password123", hasher = 'default')

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    # UNCOMMENT IF YOU WISH TO LOAD DATASETS LOCALLY

    # def add_arguments(self, parser):
    #     parser.add_argument("--main_dataset", type=str, required=True)
    #     parser.add_argument("--books_dataset", type=str, required=True)

    def handle(self, *args, **options):
        # UNCOMMENT IF YOU WISH TO LOAD DATASETS LOCALLY

        # main_dataset = pd.read_csv(options['main_dataset']).drop(columns='Unnamed: 0')
        # books_dataset = pd.read_csv(options['books_dataset']).drop(columns='Unnamed: 0')

        # UNCOMMENT IF YOU WISH TO LOAD DATASETS FROM URL
        # Paste the most up to date url links to the datasets here

        main_dataset_url = "https://media.githubusercontent.com/media/Fandasman/SEG-major-project/main/main-data.csv?token=AK35BWRBTE7O6ILWA4P3KG3CK5SBE"
        books_dataset_url = "https://media.githubusercontent.com/media/Fandasman/SEG-major-project/main/new-books-data.csv?token=AK35BWXBLPSQMDKDEV3SUI3CK5SA2"
        main_dataset = pd.read_csv(main_dataset_url, sep = ',', nrows=2000)
        books_dataset = pd.read_csv(books_dataset_url, sep = ',')

        print("Starting seed...")

        Command.generate_users(self, main_dataset)

        Command.get_books(self, books_dataset)

        Command.get_ratings(self, main_dataset)

        Command.update_genres_preferences(self)

        Command.generate_clubs(self)

        print("Seeding complete!")


    # Generate fake users
    def generate_users(self, main_dataset):
        print("Generating club owner profile...")
        num_user_ids = 500
        User.objects.create(
            id = 1,
            username = 'charlie',
            first_name = 'Charlie',
            last_name = 'Czechman',
            email = 'charlie@example.org',
            password = Command.PASSWORD,
            bio = 'Hi, I own all the clubs here. Care to join?'
        )

        print("Done!")

        print("Generating fake users...")
        for i in tqdm(range(num_user_ids - 1)):
            fakeUsername = self.faker.user_name() + str(i)
            fakeFirstName = self.faker.first_name()
            fakeLastName = self.faker.last_name()
            fakeEmail = fakeUsername + "@example.org"
            fakeBio = self.faker.text(max_nb_chars = 500)

            User.objects.create(
                id = i + 2,
                username = fakeUsername,
                first_name = fakeFirstName,
                last_name = fakeLastName,
                email = fakeEmail,
                password = Command.PASSWORD,
                bio = fakeBio
            )

        print("Done!")


    # Read ratings from the main dataset
    def get_ratings(self, main_dataset):
        print("Reading ratings from the main dataset...")

        for index, row in tqdm(main_dataset.iterrows(), total=main_dataset.shape[0]):
            user_id = row['User-ID']
            if user_id in User.objects.values_list('id', flat=True):
                BooksRatings.objects.create(
                    isbn = row['ISBN'],
                    rating = row['Book-Rating'],
                    user = User.objects.get(id=row['User-ID'])
                )

        print("Done!")


    # Read books from the dataset
    def get_books(self, books_dataset):
        print("Reading books from the dataset...")

        for index, row in tqdm(books_dataset.iterrows(), total=books_dataset.shape[0]):
            Book.objects.create(
                isbn = row['ISBN'],
                title = row['Book-Title'],
                author = row['Book-Author'],
                published = row['Year-Of-Publication'],
                publisher = row['Publisher'],
                genre = row['Genres'],
                imgURLSmall = row['Image-URL-S'],
                imgURLMedium = row['Image-URL-M'],
                imgURLLarge = row['Image-URL-L']
            )

        print("Done!")

    # Update the genres preferences of current users
    def update_genres_preferences(self):
        print("Updating the genres preferences of current users...")

        for user in tqdm(User.objects.all()):
            user_genres = Book.objects.filter(isbn__in = user.users.values('isbn')).values_list('genre', flat=True).distinct()
            for i in range(len(user_genres)):
                user.genres_preferences.insert(i, user_genres[i])
            user.save()

        print("Done!")


    # Generate fake clubs and set charlie as their owner
    def generate_clubs(self):
        print("Generating fake book clubs...")
        for i in tqdm(range(20)):
            fakeName = self.faker.company()
            fakeLocation = self.faker.address(max_nb_chars = 100)
            fakeDescription = self.faker.text(max_nb_chars = 500)
            club_book = Book.objects.get(id=random.randint(1, len(Book.objects.all())))

            club = Club.objects.create(
                name = fakeName,
                location = fakeLocation,
                description = fakeDescription,
                club_book = club_book
            )

            Role.objects.create(
                user = User.objects.get(username = "charlie"),
                club = club,
                role = 'CO'
            )

            for i in range(random.randint(2, 3)):
                user = User.objects.get(id=random.randint(2, len(User.objects.all())))
                club_roles = Role.objects.filter(club = club)
                club_user_ids = [i['user_id'] for i in club_roles.values('user_id')]

                if user.id not in club_user_ids:
                    Role.objects.create(
                        user = user,
                        club = club,
                        role = 'O'
                    )

            for i in range(random.randint(5, 10)):
                user = User.objects.get(id=random.randint(2, len(User.objects.all())))
                club_roles = Role.objects.filter(club = club)
                club_user_ids = [i['user_id'] for i in club_roles.values('user_id')]

                if user.id not in club_user_ids:
                    Role.objects.create(
                        user = user,
                        club = club,
                        role = 'M'
                    )

        print("Done!")
