from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description','isbn', 'publication_date', 'category', 'genre', 'copies_available', 'cover_image', 'book_file']
        widgets = {
            'genre': forms.CheckboxSelectMultiple(),
        }
