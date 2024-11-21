import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management_system.settings')
django.setup()

from books.models import Category, Genre

def add_icons_and_descriptions():
    # Categories with descriptions and icon classes
    categories_with_icons = {
        "Fiction": {"description": "Stories that contain events created from the imagination.", "icon": "fas fa-book-open"},
        "Non-Fiction": {"description": "Books based on real events, people, or facts.", "icon": "fas fa-book"},
        "Science": {"description": "Books exploring scientific concepts, discoveries, and research.", "icon": "fas fa-flask"},
        "History": {"description": "Literature focused on past events and historical figures.", "icon": "fas fa-history"},
        "Education": {"description": "Resources aimed at learning and academic development.", "icon": "fas fa-chalkboard-teacher"},
        "Technology": {"description": "Books on innovations and advancements in technology.", "icon": "fas fa-laptop"},
        "Romance": {"description": "Stories focusing on love and relationships.", "icon": "fas fa-heart"},
        "Biography": {"description": "Accounts of someone's life written by someone else.", "icon": "fas fa-user-alt"},
        "Fantasy": {"description": "Books featuring magical worlds, creatures, and adventures.", "icon": "fas fa-magic"},
        "Mystery": {"description": "Stories centered around solving crimes or uncovering secrets.", "icon": "fas fa-search"},
        "Thriller": {"description": "Books that evoke excitement and suspense.", "icon": "fas fa-bolt"},
        "Horror": {"description": "Frightening stories meant to invoke fear or unease.", "icon": "fas fa-ghost"},
        "Self-Help": {"description": "Guides to personal development and self-improvement.", "icon": "fas fa-users"},
        "Health": {"description": "Books on physical and mental wellness.", "icon": "fas fa-heartbeat"},
        "Travel": {"description": "Literature exploring destinations and journeys.", "icon": "fas fa-plane"},
        "Cooking": {"description": "Guides and recipes for preparing meals and cuisines.", "icon": "fas fa-utensils"},
        "Art": {"description": "Books about art history, techniques, and artists.", "icon": "fas fa-palette"},
        "Religion": {"description": "Texts focusing on spiritual beliefs and practices.", "icon": "fas fa-praying-hands"},
        "Business": {"description": "Books on entrepreneurship, management, and finance.", "icon": "fas fa-briefcase"},
        "Sports": {"description": "Literature covering sports, athletes, and techniques.", "icon": "fas fa-basketball-ball"}
    }

    # Create or update categories with icons and descriptions
    for category_name, data in categories_with_icons.items():
        Category.objects.get_or_create(
            name=category_name,
            defaults={"description": data["description"], "icon": data["icon"]}
        )

    print(f"Categories with icons and descriptions added or updated.")

    # Genres with descriptions and icon classes
    genres_with_icons = {
        "Adventure": {"description": "Exciting and risk-taking stories.", "icon": "fas fa-mountain"},
        "Drama": {"description": "Books focused on real-life situations and emotions.", "icon": "fas fa-theater-masks"},
        "Fantasy": {"description": "Books featuring magical and imaginary worlds.", "icon": "fas fa-magic"},
        "Historical Fiction": {"description": "Fiction set in a particular historical period.", "icon": "fas fa-calendar-alt"},
        "Horror": {"description": "Books meant to frighten or disturb the reader.", "icon": "fas fa-ghost"},
        "Humor": {"description": "Books meant to entertain with humor.", "icon": "fas fa-laugh"},
        "Mystery": {"description": "Stories focused on solving mysteries or crimes.", "icon": "fas fa-search"},
        "Poetry": {"description": "Creative and artistic use of language.", "icon": "fas fa-pen-alt"},
        "Romantic Comedy": {"description": "Humorous books centered around romance.", "icon": "fas fa-heart"},
        "Science Fiction": {"description": "Fiction based on scientific principles and technology.", "icon": "fas fa-robot"},
        "Self-Improvement": {"description": "Books focused on personal growth.", "icon": "fas fa-balance-scale"},
        "Spiritual": {"description": "Books focused on spiritual growth and enlightenment.", "icon": "fas fa-praying-hands"},
        "Suspense": {"description": "Books with tension and mystery.", "icon": "fas fa-eye"},
        "Thriller": {"description": "Books designed to keep the reader on the edge of their seat.", "icon": "fas fa-bolt"},
        "Young Adult": {"description": "Books aimed at young adult readers.", "icon": "fas fa-user-graduate"}
    }

    # Create or update genres with icons and descriptions
    for genre_name, data in genres_with_icons.items():
        Genre.objects.get_or_create(
            name=genre_name,
            defaults={"description": data["description"], "icon": data["icon"]}
        )

    print(f"Genres with icons and descriptions added or updated.")

if __name__ == '__main__':
    add_icons_and_descriptions()
