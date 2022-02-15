from django.core.management.base import BaseCommand, CommandError
from clubs.models import User, Book, Club, Role

class Command(BaseCommand):
    """The database unseeder."""

    def handle(self, *args, **options):
        print("Starting unseed...")

        Command.delete_books(self)

        Command.delete_users(self)

        Command.delete_clubs(self)

        print("Unseeding complete!")
    

    # Delete functions
    def delete_books(self):
        print("Deleting books...")

        books = Book.objects.all()
        for book in books:
            book.delete()

        print("Done!")

    def delete_clubs(self):
        print("Deleting clubs...")

        clubs = Club.objects.all()
        for club in clubs:
            club.delete()

        print("Done!")

    def delete_users(self):
        print("Deleting users...")
        users = User.objects.exclude(username__icontains = "admin")
        for user in users:
            user.delete()
        print("Done!")