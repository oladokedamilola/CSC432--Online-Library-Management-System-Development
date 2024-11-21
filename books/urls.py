from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='books'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('categories/', views.category, name='category_books'),
    path('genres/', views.genre, name='genre_books'),
    path('category/<int:category_id>/', views.category_books, name='category_books'),
    path('genre/<int:genre_id>/', views.genre_books, name='genre_books'),
    path('search/', views.search_books, name='search_books'),

    path('read/<int:pk>/', views.read_book, name='read_book'),
    path('book/<int:book_id>/status/<str:field>/', views.update_book_status, name='update_book_status'),
    path('download/<int:book_id>/', views.download_book, name='download_book'),

    path('add-book/', views.add_book, name='add_book'),




]
