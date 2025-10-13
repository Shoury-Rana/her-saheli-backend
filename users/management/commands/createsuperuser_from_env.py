import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser from environment variables (ADMIN_USERNAME, ADMIN_PASSWORD)'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME')
        password = os.environ.get('ADMIN_PASSWORD')

        if not username or not password:
            self.stdout.write(self.style.ERROR(
                'ADMIN_USERNAME and ADMIN_PASSWORD environment variables must be set.'
            ))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(
                f'Superuser "{username}" already exists. Skipping creation.'
            ))
        else:
            User.objects.create_superuser(username=username, password=password)
            self.stdout.write(self.style.SUCCESS(
                f'Successfully created superuser "{username}"'
            ))