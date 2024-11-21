from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
import uuid


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'country', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'country', 'reference_id')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'country')}),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.reference_id:
            obj.reference_id = str(uuid.uuid4())
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserInterest)
admin.site.register(Onboarding)
