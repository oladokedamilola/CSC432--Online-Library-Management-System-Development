from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Book
from users.models import Reader
from .forms import BookForm
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required



@login_required
def books_list(request):
    query = request.GET.get('query')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all().order_by('title')  # Order books by title

    # Handle the book addition form
    if request.method == 'POST' and 'add_book' in request.POST:
        form = BookForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('books')  # Redirect to the books list page
        else:
            messages.error(request, 'Error adding book. Please check the form.')
    else:
        form = BookForm()

    # Pagination
    paginator = Paginator(books, 10)  # Show 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'books/books.html', {'page_obj': page_obj, 'form': form})

@login_required
def add_to_bag(request, book_id):
    if 'cart' not in request.session:
        request.session['cart'] = []
    cart = request.session['cart']
    if book_id not in cart:
        cart.append(book_id)
    request.session['cart'] = cart
    return redirect('books')

@login_required
def mybag_modal(request):
    cart = request.session.get('cart', [])
    books_in_bag = Book.objects.filter(pk__in=cart)
    return render(request, 'mybag_modal.html', {'books': books_in_bag})
