from django.contrib import admin
from .models import *

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'get_genres', 'copies_available')
    list_filter = ('category', 'genre', 'author')
    search_fields = ('title', 'author', 'isbn')

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
    get_genres.short_description = 'Genres'

admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(UserBook)