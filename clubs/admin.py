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
        'isbn', 'title', 'author', 'publisher', 'published', 'imgURLSmall', 'imgURLMedium', 'imgURLLarge'
    ]

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'leader', 'get_members', 'location', 'description'
    ]