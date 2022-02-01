from django.contrib import admin
from .models import User, Book, Club

# Register User model.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'first_name', 'last_name', 'email', 'is_active',
    ]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'author', 'description', 'publisher', 'rating', 'isbn', 'genre', 'isFranchise',
    ]

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'description'
    ]