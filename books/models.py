from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    publication_date = models.DateField()
    genre = models.CharField(max_length=100)
    copies_available = models.IntegerField()
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    book_file = models.FileField(upload_to='books_files/', blank=True, null=True)

    def __str__(self):
        return self.title
