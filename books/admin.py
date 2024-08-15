from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'publication_date', 'genre', 'copies_available', 'cover_image', 'book_file')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('genre', 'publication_date')

    # Optionally add form fields for better control
    fields = ('title', 'author', 'isbn', 'publication_date', 'genre', 'copies_available', 'cover_image', 'book_file')
    # Include image preview in admin interface
    readonly_fields = ('cover_image', 'book_file')

    def cover_image_preview(self, obj):
        if obj.cover_image:
            return f'<img src="{obj.cover_image.url}" width="100" />'
        return "No Image"
    cover_image_preview.allow_tags = True
    cover_image_preview.short_description = 'Cover Image Preview'

    def book_file_size(self, obj):
        if obj.book_file:
            return f"{obj.book_file.size / 1024:.2f} KB"
        return "No File"
    book_file_size.short_description = 'Book File Size'

    # Add the custom preview and size fields to the list display
    list_display = ('title', 'author', 'isbn', 'publication_date', 'genre', 'copies_available', 'cover_image_preview', 'book_file_size')

admin.site.register(Book, BookAdmin)
