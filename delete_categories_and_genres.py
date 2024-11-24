import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management_system.settings')
django.setup()

from books.models import Category, Genre

def delete_all_categories_and_genres():
    try:
        # Confirm deletion
        confirm = input("Are you sure you want to delete all categories and genres? Type 'yes' to confirm: ")
        if confirm.lower() == 'yes':
            # Delete all categories
            categories_deleted_count, _ = Category.objects.all().delete()
            print(f"Successfully deleted {categories_deleted_count} categories.")

            # Delete all genres
            genres_deleted_count, _ = Genre.objects.all().delete()
            print(f"Successfully deleted {genres_deleted_count} genres.")
        else:
            print("Operation canceled.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    delete_all_categories_and_genres()
