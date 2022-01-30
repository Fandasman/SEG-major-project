from django.core.management.base import BaseCommand, CommandError
from clubs.models import User

class Command(BaseCommand):
    """The database unseeder."""

    def handle(self, *args, **options):
        print("Removing users...")
        users = User.objects.exclude(username__icontains = "admin")
        for user in users:
            user.delete()
        print("Done!")
