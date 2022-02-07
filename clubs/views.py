from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .models import Book, Club, User
from .forms import EditProfileForm

# Create your views here.

def feed(request):
    current_user = request.user
    return render(request, 'feed.html', {'user': current_user})

def home(request):
    return render(request, 'home.html')

# @login_required
def show_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except ObjectDoesNotExist:
        return redirect('search_books')
    else:
        return render(request, 'show_book.html',
            {'book': book}
        )

# @login_required
def show_club(request, club_id):
    try:
        club = Club.objects.get(id=club_id)
    except ObjectDoesNotExist:
        return redirect('search_clubs')
    else:
        return render(request, 'show_club.html',
            {'club': club}
        )

# @login_required
def show_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return redirect('search_users')
    else:
        return render(request, 'show_user.html',
            {'user': user}
        )

# @login_required
def search_books(request):
    search_book = request.GET.get('book_searchbar')
    if search_book:
        books= Book.objects.filter(Q(name__icontains=search_book))
    else:
        books = Book.objects.all()
    return render(request, 'search_books.html', {'books': books})

# @login_required
def search_clubs(request):
    search_club = request.GET.get('club_searchbar')
    if search_club:
        clubs= Club.objects.filter(Q(name__icontains=search_club))
    else:
        clubs = Club.objects.all()
    return render(request, 'search_clubs.html', {'clubs': clubs})

# @login_required
def search_users(request):
    search_user = request.GET.get('user_searchbar')
    if search_user:
        users= User.objects.filter(Q(username__icontains=search_user))
    else:
        users= User.objects.all()
    return render(request, 'search_users.html', {'users': users})

@login_required
def edit_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = EditProfileForm(instance=current_user, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
            return redirect('feed')
    else:
        form = EditProfileForm(instance=current_user)
    return render(request, 'edit_profile.html', {'form': form, 'user': current_user})

