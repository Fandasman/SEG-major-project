from django.core.management.base import BaseCommand, CommandError
from clubs.models import User, Club

class Command(BaseCommand):
    """The database unseeder."""

    def handle(self, *args, **options):
        print("Starting unseed...")

        Command.delete_users(self)

        Command.delete_clubs(self)

        print("Unseeding successful!")
    

    # Delete functions
    def delete_users(self):
        print("Deleting users...")
        users = User.objects.exclude(username__icontains = "admin")
        for user in users:
            user.delete()
        print("Done!")
    
    def delete_clubs(self):
        print("Deleting clubs...")

        clubs = Club.objects.all()
        for club in clubs:
            club.delete()

        print("Done!")