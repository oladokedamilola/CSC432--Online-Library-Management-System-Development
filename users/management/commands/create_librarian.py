from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a librarian user'

    def handle(self, *args, **kwargs):
        username = input('Enter librarian username: ')
        password = input('Enter librarian password: ')
        email = input('Enter librarian email: ')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.is_staff = True  # Set as staff to access admin panel
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Librarian {username} created successfully.'))
