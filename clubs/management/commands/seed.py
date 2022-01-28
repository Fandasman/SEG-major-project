from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    """The database seeder."""

    def handle(self, *args, **options):
        print("TODO: The database seeder will be added here...")
