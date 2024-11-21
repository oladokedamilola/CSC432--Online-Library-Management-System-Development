import os
import django

# Set up Django environment for standalone script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_management_system.settings")  # Replace 'library_management_system' with your actual project name
django.setup()

from users.models import UserInterest  

def populate_interests():
    # List of interests to add to the database
    interests = [
        {'name': 'Sports', 'icon': 'fas fa-football-ball'},
        {'name': 'Music', 'icon': 'fas fa-music'},
        {'name': 'Travel', 'icon': 'fas fa-plane'},
        {'name': 'Technology', 'icon': 'fas fa-laptop'},
        {'name': 'Art', 'icon': 'fas fa-palette'},
        {'name': 'Health', 'icon': 'fas fa-heartbeat'},
        {'name': 'Food', 'icon': 'fas fa-utensils'},
        {'name': 'Education', 'icon': 'fas fa-book'},
        {'name': 'Gaming', 'icon': 'fas fa-gamepad'},
        {'name': 'Literature', 'icon': 'fas fa-book-open'}
    ]

    # Add each interest to the UserInterest model if it doesn't already exist
    for interest_data in interests:
        interest, created = UserInterest.objects.get_or_create(
            name=interest_data['name'],
            defaults={'icon': interest_data['icon']}
        )
        if created:
            print(f"Added interest: {interest_data['name']}")
        else:
            print(f"Interest '{interest_data['name']}' already exists in the database.")

if __name__ == "__main__":
    populate_interests()
