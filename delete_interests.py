import os
import django

# Set up Django environment for standalone script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_management_system.settings")  # Replace 'library_management_system' with your actual project name
django.setup()

from users.models import UserInterest  

def delete_all_interests():
    # Confirm deletion with the user
    confirm = input("Are you sure you want to delete all entries in UserInterest? Type 'yes' to confirm: ")
    if confirm.lower() == 'yes':
        deleted_count, _ = UserInterest.objects.all().delete()
        print(f"Deleted {deleted_count} entries from UserInterest.")
    else:
        print("Deletion canceled.")

if __name__ == "__main__":
    delete_all_interests()
