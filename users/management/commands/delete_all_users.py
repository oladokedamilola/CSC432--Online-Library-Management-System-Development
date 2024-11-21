from django.core.management.base import BaseCommand
from users.models import CustomUser 

class Command(BaseCommand):
    help = "Delete all users in the CustomUser model"

    def handle(self, *args, **kwargs):
        CustomUser.objects.all().delete()
        self.stdout.write("All users have been deleted.")
