"""
Django command to wait for the database to be available.
"""

from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
import time


class Command(BaseCommand):
    """Django command to wait for the database."""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        db_ready = False
        self.stdout.write("Checking the database...")
        while db_ready is False:
            try:
                self.check(databases=['default'])
                db_ready = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write(
                    'Database is not available, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database is available!"))
