from django.contrib import admin
from .models import User, Book, Club, Role, Invitation,Event, EventPost, UserPost, MembershipPost, Comment


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

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
         'name', 'deadline'
    ]
@admin.register(EventPost)
class EventPostAdmin(admin.ModelAdmin):
    list_display = [
         'event', 'user', 'created_at'
    ]
@admin.register(UserPost)
class UserPostAdmin(admin.ModelAdmin):
    list_display = [
         'author', 'text', 'created_at'
    ]
@admin.register(MembershipPost)
class MembershipPostAdmin(admin.ModelAdmin):
    list_display = [
         'user', 'club', 'join', 'created_at'
    ]
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
         'body', 'club', 'post', 'created_at'
    ]
