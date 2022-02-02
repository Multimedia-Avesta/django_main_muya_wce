"""
Ensure a superuser defined by DJANGO_SUPERUSER_USERNAME exists

Like the built-in `createsuperuser --noinput`, except that the command does not
fail if the user already exists.

Set the envars DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD and
optionally DJANGO_SUPERUSER_EMAIL.

Author: Hal Blackburn <hwtb2@cam.ac.uk>
"""
import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = __doc__.strip().splitlines()[0]

    def handle(self, **kwargs):
        user = os.environ.get('DJANGO_SUPERUSER_USERNAME') or None
        pw = os.environ.get('DJANGO_SUPERUSER_PASSWORD') or None
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL') or None

        if not (user and pw):
            return

        User = get_user_model()
        if User.objects.filter(email=email).exists():
            return

        User.objects.create_superuser(username=user, password=pw, email=email)
        self.stdout.write(self.style.SUCCESS(f"Superuser {user!r} created successfully"))
