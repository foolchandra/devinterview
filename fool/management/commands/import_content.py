from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Import from content.json into the database"

    def handle(self, *args, **kwargs):
        connection = None

