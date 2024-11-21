from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
import os
from .forms import *
from django.http import JsonResponse
from django.db import transaction



def book_list(request):
    # Fetch all books
    books = Book.objects.all()

    # Fetch categories and genres
    categories = Category.objects.all()
    genres = Genre.objects.all()

    # Pagination
    paginator = Paginator(books, 9)  # 9 books per page
    page = request.GET.get('page')  # Get the current page number
    books = paginator.get_page(page)

    # Context to pass to the template
    context = {
        'books': books,
        'categories': categories,
        'genres': genres,
    }

    return render(request, 'books/books.html', context)

def category(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'books/all_categories.html', context)

def genre(request):
    genres = Genre.objects.all()
    context = {
        'genres': genres,
    }
    return render(request, 'books/all_genres.html', context) 

def category_books(request, category_id):
    category = Category.objects.get(id=category_id)
    books = Book.objects.filter(category=category)

    # Pagination
    paginator = Paginator(books, 9)  # 9 books per page
    page = request.GET.get('page')
    books = paginator.get_page(page)

    context = {
        'books': books,
        'category': category,
    }
    return render(request, 'books/category_books.html', context)

def genre_books(request, genre_id):
    genre = Genre.objects.get(id=genre_id)
    books = Book.objects.filter(genre=genre)

    # Pagination
    paginator = Paginator(books, 9)  # 9 books per page
    page = request.GET.get('page')
    books = paginator.get_page(page)

    context = {
        'books': books,
        'genre': genre,
    }
    return render(request, 'books/genre_books.html', context)

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, id=pk)
    userbook = book.userbook_set.filter(user=request.user).first()  # Get the first matching userbook
    
    return render(request, 'books/book_detail.html', {'book': book, 'userbook': userbook})

def read_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/read_online.html', {'book': book})

from django.shortcuts import render
from .models import Book, Category, Genre
from django.db.models import Q  # For combining filters with OR condition

def search_books(request):
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()
    genre_id = request.GET.get('genre', '').strip()

    # Get all books initially
    books = Book.objects.all()

    # Filter by query if provided
    if query:
        books = books.filter(title__icontains=query)

    # Apply filtering by category or genre with OR logic
    filters = Q()  # Empty Q object to combine conditions
    
    if category_id:
        filters |= Q(category_id=category_id)  # Add OR condition for category filter

    if genre_id:
        filters |= Q(genre__id=genre_id)  # Add OR condition for genre filter
    
    if filters:
        books = books.filter(filters)  # Apply the combined OR condition

    # For form population
    categories = Category.objects.all()
    genres = Genre.objects.all()

    context = {
        'books': books,
        'categories': categories,
        'genres': genres,
        'query': query,
        'selected_category': category_id,
        'selected_genre': genre_id,
    }
    return render(request, 'books/search.html', context)



@login_required
def update_book_status(request, book_id, field):
    # Get the book instance
    book = get_object_or_404(Book, pk=book_id)

    try:
        # Get or create the UserBook instance for the logged-in user and the current book
        userbook, created = UserBook.objects.get_or_create(user=request.user, book=book)

        # Use a transaction to ensure atomic updates
        with transaction.atomic():
            # Check and update the status only if it hasn't been set already
            if field == 'liked':
                userbook.liked = not userbook.liked  # Toggle the liked status
            elif field == 'read':
                if not userbook.read:
                    userbook.read = True  # Mark as read
            elif field == 'downloaded':
                if not userbook.downloaded:
                    userbook.downloaded = True  # Mark as downloaded

            # Save the updated UserBook instance
            userbook.save()

        # Return a JSON response with the updated status
        return JsonResponse({
            'liked': userbook.liked,
            'read': userbook.read,
            'downloaded': userbook.downloaded
        })

    except Exception as e:
        # Log the error if necessary and return a 500 error response
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def download_book(request, book_id):
    # Get the book instance from the database
    book = get_object_or_404(Book, pk=book_id)

    # Get the file path of the book file
    if not book.book_file:
        return JsonResponse({'error': 'No file available for download'}, status=404)

    file_path = book.book_file.path
    
    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')  # Adjust MIME type if necessary
            response['Content-Disposition'] = f'attachment; filename="{book.title}.pdf"'  # Adjust the file name as needed
            return response
    else:
        return JsonResponse({'error': 'File not found'}, status=404)

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully!")
            return redirect('add_book')  # Redirect to the same page or another one
    else:
        form = BookForm()
    
    return render(request, 'books/add_book.html', {'form': form})
