from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from .forms import SignUpForm
from .forms import CreateClubForm
from django.conf import settings
from .models import Book, Club, User


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


    # class LoginProhibitedMixin:
    #
    #      """Mixin that redirects when a user is logged in."""
    #
    #      redirect_when_logged_in_url = None
    #
    #      def dispatch(self, *args, **kwargs):
    #         """Redirect when logged in, or dispatch as normal otherwise."""
    #         if self.request.user.is_authenticated:
    #             return self.handle_already_logged_in(*args, **kwargs)
    #         return super().dispatch(*args, **kwargs)
    #
    #      def handle_already_logged_in(self, *args, **kwargs):
    #          url = self.get_redirect_when_logged_in_url()
    #          return redirect(url)
    #
    #      def get_redirect_when_logged_in_url(self):
    #          """Returns the url to redirect to when not logged in."""
    #          if self.redirect_when_logged_in_url is None:
    #             raise ImproperlyConfigured(
    #              "LoginProhibitedMixin requires either a value for "
    #              "'redirect_when_logged_in_url', or an implementation for "
    #              "'get_redirect_when_logged_in_url()'."
    #              )
    #          else:
    #              return self.redirect_when_logged_in_url


    """This function standardize the requirements for
        user registration, if the user successfully
        registers, it will be created in the system,
        and will be redirected to the profile page """
class SignUpView(FormView):
    """View that signs up user."""

    form_class = SignUpForm()
    template_name = "sign_up.html"
    #redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        pass
        #return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


"""This function standardize the requirements for
    creating clubs, if club is successfully created,
    it will be store in the database and client will
    be redirected to the feed page"""
def CreateClubView(request):
    if request.method == "POST":
        form = CreateClubForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/feed/')
    else:
        form = CreateClubForm()
    return render(request, 'create_club.html', {'form': form})
