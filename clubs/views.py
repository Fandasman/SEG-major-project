from django import template
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from .forms import SignUpForm, LogInForm, EditProfileForm, ClubForm, SetClubBookForm
from .models import Book, Club, Role, User

# Create your views here.

def feed(request):
    current_user = request.user
    return render(request, 'feed.html', {'user': current_user})

class LoginProhibitedMixin:
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('feed')
        return super().dispatch(*args, **kwargs)

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
def profile(request):
    current_user = request.user
    return render(request, 'profile.html',
            {'user': current_user}
        )

# @login_required
def search_books(request):
    search_book = request.GET.get('book_searchbar')
    if search_book:
        books= Book.objects.filter(Q(name__icontains=search_book))
    else:
        books = Book.objects.all()
    return render(request, 'search_books.html', {'books': books})


def set_club_book(request):
    current_user = request.user

    if request.method == 'POST':
        form = SetClubBookForm(request.POST)
        if form.is_valid():
            club = form.get_club()
            book = form.get_book()
            #current_owned_clubs = Role.objects.filter(user=current_user, role='O')
            #if club in current_owned_clubs:
            club._add_book(book)
            return redirect('login')
            #else:
                #messages.add_message(request, messages.ERROR, "you don't own this club")
               # form = SetClubBookForm()
        else:
            messages.add_message(request, messages.ERROR, "Invalid club name or book name")
            form = SetClubBookForm()
        return render(request, 'set_club_book.html', {'form' : form})
    else:
        form = SetClubBookForm()
        return render(request, 'set_club_book.html', {'form': form})


@login_required
def create_club(request):
    current_user = request.user
    if request.method == 'POST':
        current_user = request.user
        current_owned_clubs = Role.objects.filter(user = current_user, role = 'O')
        if len(current_owned_clubs) < 3:
            form = ClubForm(request.POST)
            if form.is_valid():
                newClub = form.save()
                role = Role.objects.create(user = current_user, club = newClub, role = 'O')
                return redirect('club_list')
        else:
            messages.add_message(request, messages.ERROR, "You already own too many clubs!")
            form = ClubForm()
        return render(request, 'create_club.html' , {'form': form})

    else:
        form = ClubForm()
        return render(request, 'create_club.html' , {'form': form})
# class FeedView(LoginRequiredMixin, ListView):
#     """Class-based generic view for displaying a view."""
#
#     model = Post
#     template_name = "feed.html"
#     context_object_name = 'posts'
#
#     def get_queryset(self):
#         """Return the user's feed."""
#         current_user = self.request.user
#         authors = list(current_user.followees.all()) + [current_user]
#         posts = Post.objects.filter(author__in=authors)
#         return posts
#
#     def get_context_data(self, **kwargs):
#         """Return context data, including new post form."""
#         context = super().get_context_data(**kwargs)
#         context['user'] = self.request.user
#         context['form'] = ClubForm()
#         return context

class HomeView(LoginProhibitedMixin,View):
    template_name = 'home.html'

    def get(self,request):
        return self.render()

    def post(self,request):
        return self.render()

    def render(self):
        return render(self.request, 'home.html')

# class MemberListView(LoginRequiredMixin, ListView):
class MemberListView(ListView):
    model= User
    template_name= 'member_list.html'
    context_object_name= 'users'

    # def get_context_data(self, *args, **kwargs):
    #     context= super().get_context_data(*args, **kwargs)
    #     user= User.objects.all()
    #     context['members']= Role.objects.all().filter(role= "M")
    #     return context

# class ClubListView(LoginRequiredMixin, ListView):
class ClubListView(ListView):
    model= Club
    template_name= 'club_list.html'
    context_object_name= 'clubs'

    def get_context_data(self, *args, **kwargs):
        context= super().get_context_data(*args, **kwargs)
        club= Club.objects.all()
        context['roles']= Role.objects.all().filter(role= "O")
        return context

# class OwnerClubListView(LoginRequiredMixin, ListView):
class OwnerClubListView(ListView):
    model= Club
    template_name= 'owner_club_list.html'
    context_object_name= 'user'

    def get_context_data(self, *args, **kwargs):
        context= super().get_context_data(*args, **kwargs)
        current_user= self.request.user
        context['roles']= Role.objects.all().filter(user= current_user, role= "O")
        return context

# class MemberClubListView(LoginRequiredMixin, ListView):
class MemberClubListView(ListView):
    model= Club
    template_name= 'member_club_list.html'
    context_object_name= 'user'

    def get_context_data(self, *args, **kwargs):
        context= super().get_context_data(*args, **kwargs)
        current_user= self.request.user
        context['roles']= Role.objects.all().filter(user= current_user, role= "M")
        return context


class ShowUserView(DetailView):
    model = User
    template_name = 'show_user.html'
    pk_url_kwarg = "user_id"

class ShowClubView(DetailView):
    model = Club
    template_name = 'show_club.html'
    pk_url_kwarg = "club_id"


# class LoginProhibitedMixin:

#          """Mixin that redirects when a user is logged in."""

#          redirect_when_logged_in_url = None

#          def dispatch(self, *args, **kwargs):
#             """Redirect when logged in, or dispatch as normal otherwise."""
#             if self.request.user.is_authenticated:
#                 return self.handle_already_logged_in(*args, **kwargs)
#             return super().dispatch(*args, **kwargs)

#          def handle_already_logged_in(self, *args, **kwargs):
#              url = self.get_redirect_when_logged_in_url()
#              return redirect('feed')

#          def get_redirect_when_logged_in_url(self):
#              """Returns the url to redirect to when not logged in."""
#              if self.redirect_when_logged_in_url is None:
#                 raise ImproperlyConfigured(
#                  "LoginProhibitedMixin requires either a value for "
#                  "'redirect_when_logged_in_url', or an implementation for "
#                  "'get_redirect_when_logged_in_url()'."
#                  )
#              else:
#                  return self.redirect_when_logged_in_url

class LogInView(View):
    """Log-in handling view"""
    def get(self,request):
        self.next = request.GET.get('next') or 'officer'
        return self.render()

    def post(self,request):
        form = LogInForm(request.POST)
        self.next = request.POST.get('next')
        user = form.get_user()
        if user is not None:
                """Redirect to club selection page, with option to create new club"""
                login(request, user)
                return redirect('feed')

        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        form = LogInForm()
        return render(self.request, 'login.html', {'form': form, 'next' : self.next})

"""View used for logging out."""
def log_out(request):
    logout(request)
    return redirect('home')

"""This function standardize the requirements for
    user registration, if the user successfully
    registers, it will be created in the system,
    and will be redirected to the profile page """
class SignUpView(FormView):
    """View that signs up user."""

    form_class = SignUpForm
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
@login_required
def create_club(request):
    current_user = request.user
    if request.method == 'POST':
        current_user = request.user
        current_owned_clubs = Role.objects.filter(user = current_user, role = 'O')
        if len(current_owned_clubs) < 3:
            form = ClubForm(request.POST)
            if form.is_valid():
                newClub = form.save()
                role = Role.objects.create(user = current_user, club = newClub, role = 'O')
                return redirect('club_list')
        else:
            messages.add_message(request, messages.ERROR, "You already own too many clubs!")
            form = ClubForm()
        return render(request, 'create_club.html' , {'form': form})

    else:
        form = ClubForm()
        return render(request, 'create_club.html' , {'form': form})



class EditProfileView(View):
    def get(self,request):
        return self.render()

    def post(self,request):
        current_user = request.user
        form = EditProfileForm(instance=current_user, data=request.POST)
        if form.is_valid():
            current_user.username = form.cleaned_data.get('username')
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
            return redirect('feed')
        return render(request, 'edit_profile.html', {'form': form, 'user': current_user})

    def render(self):
        current_user = self.request.user
        form = EditProfileForm(instance=current_user)
        return render(self.request,'edit_profile.html', {'form': form})

"""Includes the view for a user's wishlist."""
class WishlistView(LoginRequiredMixin, ListView):
    def get(self, request, user_id):
        return self.render(user_id)

    def render(self, user_id):
        try:
            user = User.objects.get(id = user_id)
            return render(self.request, 'wishlist.html', {'user': user})

        except ObjectDoesNotExist:
            return redirect('feed')
