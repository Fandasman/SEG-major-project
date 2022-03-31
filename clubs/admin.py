from django.contrib import admin
from .models import BooksRatings, User, Book, Club, Role, Invitation


# Register User model.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'first_name', 'last_name', 'email', 'get_wishlist', 'is_active',
    ]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        'isbn', 'title', 'author', 'publisher', 'published', 'imgURLSmall', 'imgURLMedium', 'imgURLLarge'
    ]

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'location', 'description',
    ]

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'get_club_name', 'role',
    ]

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'club', 'status',
    ]

@admin.register(BooksRatings)
class BookRatingsAdmin(admin.ModelAdmin):
    list_display = [
        'isbn', 'rating', 'user',
    ]