from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.books_list, name='books'),
    path('books/add/<int:book_id>/', views.add_to_bag, name='add_to_bag'),    
    path('mybag_modal/', views.mybag_modal, name='mybag_modal'),
]
