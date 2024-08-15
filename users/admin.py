from django.contrib import admin
from .models import Reader, Librarian

@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'reference_id', 'is_active')
    search_fields = ('name', 'reference_id')
    list_filter = ('is_active',)

@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at',)
    search_fields = ('user__username', 'user__email')
    list_filter = ('created_at',)
