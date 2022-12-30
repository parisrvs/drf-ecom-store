"""
Django command to wait for the database to be available
"""

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from typing import Any, Optional
from psycopg2 import OperationalError as Psycopg2Error
import time


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        """Entrypoint for the command."""

        self.stdout.write("waiting for database....")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write(
                    "Database unavailable, waiting for 1 second..."
                )
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
