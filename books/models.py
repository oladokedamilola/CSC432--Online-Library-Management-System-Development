from django.db import models
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)  # Optional description field
    icon = models.CharField(max_length=100, blank=True, null=True)  # CSS class for icons

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)  # CSS class for icons

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    genre = models.ManyToManyField(Genre, related_name='books')
    copies_available = models.IntegerField()
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    book_file = models.FileField(upload_to='book_files/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # New description field


    def __str__(self):
        return self.title


class UserBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)  # Track whether the book is liked
    read = models.BooleanField(default=False)  # Track whether the book is read
    downloaded = models.BooleanField(default=False)  # Track whether the book is downloaded"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.status}"

    class Meta:
        unique_together = ['user', 'book']  # Ensure a user cannot have multiple statuses for the same book