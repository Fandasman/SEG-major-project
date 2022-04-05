import calendar
import csv
import sys
from collections import Counter
from calendar import HTMLCalendar, c
from datetime import datetime, timedelta
from distutils.bcppcompiler import BCPPCompiler
from django import template
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.http import Http404, StreamingHttpResponse
from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy, resolve
from django.utils.safestring import mark_safe
from django.views import View, generic
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from itertools import chain
from scipy import spatial
from surprise import dump
from .forms import SignUpForm, LogInForm, EditProfileForm, ClubForm, SetClubBookForm, InviteForm,EventForm, UserPostForm, CommentForm, SearchForm, GenreForm, RatingForm
from .models import Book, Club, Role, User, Invitation, Event, EventPost, UserPost, MembershipPost, Comment, Message, BooksRatings

if "runserver" in sys.argv:
    print("Loading the model!")
    _, model = dump.load('./model.pkl')

THRESHOLD = 25


# Create your views here.
@login_required
def feed(request):
    current_user = request.user
    user_books = Book.objects.filter(isbn__in = current_user.users.values('isbn')).values_list('isbn', flat=True)
    user_genres = list(current_user.genres_preferences)
    filtered_user_books = Book.objects.exclude(isbn__in = user_books)

    recommended_books = []

    if len(user_books) < THRESHOLD:

        """Generate a query for books with the most positive ratings based on genre preferences"""

        filtered_user_genres = filtered_user_books.filter(genre__in = user_genres).values_list('isbn', flat=True)
        filtered_user_genres = BooksRatings.objects.filter(isbn__in = filtered_user_genres)
        good_isbns = list(filtered_user_genres.filter(rating__gte = 4).values_list('isbn'))
        good_sorted = [rating for ratings, c in Counter(good_isbns).most_common()
                  for rating in [ratings] * c]
        good_ratings = list(dict.fromkeys(good_sorted))[:30]

        for rating in good_ratings:
            book = Book.objects.get(isbn = rating[0])
            recommended_books.append(book)

    else:
        """Generate a query for the recommended books"""

        filtered_user_genres = filtered_user_books.filter(genre__in = user_genres)

        recommendations = {}

        for book in filtered_user_genres:
            predicted_rating = model.predict(uid=current_user.id, iid=book.isbn).est
            recommendations[book.isbn] = predicted_rating

        sorted_ratings = list(recommendations.items())
        sorted_ratings.sort(key=lambda k: k[1], reverse=True)

        for pair in sorted_ratings[:30]:
            book = Book.objects.get(isbn = pair[0])
            recommended_books.append(book)

    return render(request, 'feed.html', {'user': current_user, 'recommended_books': recommended_books})

class LoginProhibitedMixin:

  def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('feed')
        return super().dispatch(*args, **kwargs)


@login_required
def show_book(request, book_id):
    current_user = request.user
    try:
        book = Book.objects.get(id=book_id)
        in_wishlist = current_user.wishlist.filter(isbn=book.isbn).exists()
    except ObjectDoesNotExist:
        return redirect('book_list')
    else:
        book_form = RatingForm(request.POST)
        exist_rating = len(list(BooksRatings.objects.filter(isbn = book.isbn, user = current_user))) != 0
        current_rating_value = 0
        if exist_rating:
            past_rating = BooksRatings.objects.get(isbn = book.isbn, user = current_user)

        if request.method=='POST':
            if book_form.is_valid() and book_form.cleaned_data.get('rating') != '':
                if exist_rating == False:
                    new_rating = BooksRatings.objects.create(
                        isbn = book.isbn,
                        rating = book_form.cleaned_data.get('rating'),
                        user = current_user
                    )
                    new_rating.save()
                    exist_rating = True
                    current_rating_value = new_rating.rating
                    if book.genre not in current_user.genres_preferences:
                        current_user.genres_preferences.insert(len(current_user.genres_preferences), book.genre)
                        current_user.save()
                else:
                    past_rating.rating = book_form.cleaned_data.get('rating')
                    current_rating_value = past_rating.rating
                    past_rating.save()

        else:

            if exist_rating:
                current_rating_value = past_rating.rating

        return render(request, 'book_templates/show_book.html',
                     {'book': book,'form': book_form,
                     'book_id': book_id,
                     'exist_rating': exist_rating,
                     'current_rating_value': current_rating_value,
                     'in_wishlist': in_wishlist}
    )

# class ShowBookView(DetailView):

#     model = Book
#     template_name = 'show_book.html'
#     context_object_name = 'book'
#     pk_url_kwarg = 'book_id'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         book = self.get_object()
#         context['past_rating'] = BooksRatings.objects.get(isbn = book.isbn, user = self.current_user)
#         context

#     def post(self,request):
#         book_form = RatingForm(request.POST)
#         if book_form.is_valid() and book_form.cleaned_data.get('rating') != '':
#                 if exist_rating == False:
#                     new_rating = BooksRatings.objects.create(
#                         isbn = book.isbn,
#                         rating = book_form.cleaned_data.get('rating'),
#                         user = current_user
#                     )
#                     new_rating.save()
#                     exist_rating = True
#                     current_rating_value = new_rating.rating
#                     if book.genre not in current_user.genres_preferences:
#                         current_user.genres_preferences.insert(len(current_user.genres_preferences), book.genre)
#                         current_user.save()
#                 else:
#                     past_rating.rating = book_form.cleaned_data.get('rating')
#                     current_rating_value = past_rating.rating
#                     past_rating.save()




@login_required
def remove_rating(request, book_id):
    try:
        book = Book.objects.get(id = book_id)
    except ObjectDoesNotExist:
        return redirect('book_list')

    exist_rating = len(list(BooksRatings.objects.filter(isbn = book.isbn, user = request.user))) != 0
    if exist_rating:
        rating = BooksRatings.objects.get(isbn = book.isbn, user = request.user)
        rating.delete()

    return redirect('show_book', book_id)


# class RemoveRatingView(View):

#     def get(self,*args, **kwargs):
#         self.render()
    
#     def post(self,*args, **kwargs):
#         self.render()

    
#     def render(self,*args, **kwargs):
#         book_id = self.kwargs['book_id']
#         try:
#             book = Book.objects.get(id = book_id)
#         except ObjectDoesNotExist:
#             return redirect('book_list')

#         exist_rating = len(list(BooksRatings.objects.filter(isbn = book.isbn, user = self.request.user))) != 0
#         if exist_rating:
#             rating = BooksRatings.objects.get(isbn = book.isbn, user = self.request.user)
#             rating.delete()

#         return redirect('show_book', book_id)



# @login_required
# def profile(request):
#     current_user = request.user
#     return render(request, 'user_templates/profile.html',
#             {'user': current_user}
#         )


class HomeView(LoginProhibitedMixin,View):
    template_name = 'home.html'

    def get(self,request):
        return self.render()

    def post(self,request):
        return self.render()

    def render(self):
        return render(self.request, 'home.html')


class BookListView(LoginRequiredMixin, ListView):
    model= Book
    template_name= 'book_templates/book_list.html'
    context_object_name= 'books'
    paginate_by = settings.BOOKS_PER_PAGE
    ordering = ['title']

    def get_context_data(self, *args, **kwargs):
        context= super().get_context_data(*args, **kwargs)
        book= Book.objects.all()
        return context

class UserListView(LoginRequiredMixin, ListView):
    model= User
    template_name= 'user_templates/user_list.html'
    context_object_name= 'users'
    paginate_by = settings.USERS_PER_PAGE
    ordering = ['username']

    def get_context_data(self, *args, **kwargs):
        context= super().get_context_data(*args, **kwargs)
        user= User.objects.all()
        context['roles']= Role.objects.all().filter(role= "M")
        return context

class ClubListView(LoginRequiredMixin, ListView):
    model= Club
    template_name= 'club_templates/club_list.html'
    context_object_name= 'clubs'
    paginate_by = settings.CLUBS_PER_PAGE
    ordering = ['name']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        club = Club.objects.all()
        context['roles'] = Role.objects.filter(role= "O")
        return context

class OwnerClubListView(LoginRequiredMixin, ListView):
    model= Club
    template_name= 'club_templates/owner_club_list.html'
    context_object_name= 'clubs'
    paginate_by = settings.CLUBS_PER_PAGE
    ordering = ['name']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        current_user = self.request.user
        context['roles'] = Role.objects.filter(user = current_user, role= "CO")
        return context

class MemberClubListView(LoginRequiredMixin, ListView):
    model= Club
    template_name= 'club_templates/member_club_list.html'
    context_object_name= 'clubs'
    paginate_by = settings.CLUBS_PER_PAGE
    ordering = ['name']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        current_user = self.request.user
        member_roles = Role.objects.all().filter(user= current_user, role = "M")
        officer_roles = Role.objects.all().filter(user= current_user, role = "O")
        context['roles'] = list(chain(officer_roles, member_roles))
        return context

class RecommendedClubListView(ListView):
    model = Club
    template_name = 'recommended_club_list.html'
    context_object_name = 'clubs'

    def get_club_recommendations(self):
        club_similarities = {}

        current_user = self.request.user
        user_genres = list(current_user.genres_preferences)
        user_genres_counter = Counter(user_genres)

        filtered_clubs = Club.objects.filter(club_book__genre__in = user_genres)
        for club in filtered_clubs:
            distance_sum = 0
            members = Role.objects.filter(club = club).filter(role = 'M')
            for member in members.values():
                current_member = User.objects.get(id = member['user_id'])
                member_genres = list(current_member.genres_preferences)
                member_genres_counter = Counter(member_genres)
                all_genres  = list(user_genres_counter.keys() | member_genres_counter.keys())
                user_vect = [user_genres_counter.get(word, 0) for word in all_genres]
                member_vect = [member_genres_counter.get(word, 0) for word in all_genres]
                distance_sum += 1 - spatial.distance.cosine(user_vect, member_vect)
            club_similarities[club] = distance_sum / len(members)

        sorted_clubs = list(club_similarities.items())
        sorted_clubs.sort(key=lambda k: k[1], reverse=True)

        return [i[0] for i in sorted_clubs]

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = self.get_club_recommendations()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        club = Club.objects.all()
        context['roles'] = Role.objects.all().filter(role= "O")
        return context


class ShowUserView(DetailView):
    model = User
    template_name = 'user_templates/show_user.html'
    pk_url_kwarg = "user_id"

class ShowClubView(DetailView):
    model = Club
    template_name = 'club_templates/show_club.html'
    pk_url_kwarg = "club_id"

class ShowBookView(DetailView):
    model = Book
    template_name = 'book_templates/show_book.html'
    pk_url_kwarg = "book_id"


class LogInView(View):
    """Log-in handling view"""
    def get(self,request):
        return self.render()

    def post(self,request):
        form = LogInForm(request.POST)
        user = form.get_user()
        if user is not None and len(user.genres_preferences) == 0:
            login(request, user)
            return redirect('select_genres')

        if user is not None:
                """Redirect to club selection page, with option to create new club"""
                login(request, user)
                return redirect('feed')


        else:
            messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
            return self.render()

    def render(self):
        form = LogInForm()
        return render(self.request, 'login.html', {'form': form
        # , 'next' : self.next
        })

"""View used for logging out."""
@login_required
def log_out(request):
    logout(request)
    return redirect('home')

"""This function standardize the requirements for
    user registration, if the user successfully
    registers, it will be created in the system,
    and will be redirected to the profile page """
class SignUpView(LoginProhibitedMixin,FormView):
    """View that signs up user."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    # redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        super().form_valid(form)
        return redirect('select_genres')

    def get_success_url(self):
        pass

"""This function allows the user to select prefered genres upon sign up."""
# @login_required
# def select_genres(request):

#     genres = Book.objects.values_list('genre',flat=True).distinct()
#     current_user = request.user

#     if request.method=='POST':
#             form = GenreForm(request.POST)
#             if form.is_valid():
#                     current_user.genres_preferences = form.save()
#                     current_user.save()
#                     messages.add_message(request, messages.SUCCESS, "Preferences updated!")
#                     return redirect('feed')
#             else:
#                 messages.add_message(request, messages.ERROR, "You must select a maximum of 5 choices!")
#     else:
#         form = GenreForm(instance = current_user)
#     return render(request, "select_genres.html", {'genres': genres, 'form': form})


"""This class allows the user to select prefered genres upon sign up."""
class SelectGenresView(LoginRequiredMixin,FormView):
    
    form_class = GenreForm
    template_name = "select_genres.html"
    

    def form_valid(self,form):
                    current_user = self.request.user
                    current_user.genres_preferences = form.save()
                    current_user.save()
                    messages.add_message(self.request, messages.SUCCESS, "Preferences updated!")
                    return redirect('feed')
           
    def form_invalid(self,form):
                    genres = Book.objects.values_list('genre',flat=True).distinct()
                    messages.add_message(self.request, messages.ERROR, "You must select a maximum of 5 choices!")
                    return render(self.request, "select_genres.html", {'genres': genres, 'form': form})

    



"""This function standardize the requirements for
    creating clubs, if club is successfully created,
    it will be store in the database and client will
    be redirected to the feed page"""
# @login_required
# def create_club(request):
#     current_user = request.user
#     if request.method == 'POST':
#         current_user = request.user
#         current_owned_clubs = Role.objects.filter(user = current_user, role = 'CO')
#         if len(current_owned_clubs) < 3:
#             form = ClubForm(request.POST)
#             if form.is_valid():
#                 newClub = form.save()
#                 MembershipPost.objects.create(club = newClub, user = current_user)
#                 role = Role.objects.create(user = current_user, club = newClub, role = 'CO')
#                 return redirect('club_list')
#         else:
#             messages.add_message(request, messages.ERROR, "You already own too many clubs!")
#             form = ClubForm()
#         return render(request, 'club_templates/create_club.html' , {'form': form})

#     else:
#         form = ClubForm()
#         return render(request, 'club_templates/create_club.html' , {'form': form})


class CreateClubView(LoginRequiredMixin,FormView):
    model = Club
    form_class = ClubForm
    template_name = 'club_templates/create_club.html'


 

    def form_valid(self, form):
        current_user = self.request.user
        current_owned_clubs = Role.objects.filter(user = current_user, role = 'CO')
        if len(current_owned_clubs) < 3:
                newClub = form.save()
                MembershipPost.objects.create(club = newClub, user = current_user)
                role = Role.objects.create(user = current_user, club = newClub, role = 'CO')
                return redirect('club_list')
                
        else:
                messages.add_message(self.request, messages.ERROR, "You already own too many clubs!")
                form = ClubForm()


        return self.render()
    
    def form_invalid(self):
        return self.render()

    def render(self):
        form = ClubForm()
        return render(self.request, 'club_templates/create_club.html' , {'form': form})
    



"""This function allows owners of a club to delete the club"""
# @login_required
# def delete_club(request, club_id):
#     current_user = request.user
#     club = Club.objects.get(id = club_id)
#     try:
#         role = Role.objects.get(user = current_user, club = club,role = 'CO') 
#     except ObjectDoesNotExist:
#         return redirect('feed')
#     else:
#         if role.role == 'CO':
#             return render(request, 'club_templates/delete_club.html', {'club': club})
        # return redirect("feed")


class DeleteClubView(LoginRequiredMixin,View):

    def get(self,*args, **kwargs):
        return self.render()

    def post(self,request,club_id):
        self.render()
        
    


    def render(self,*args, **kwargs):
        club_id = self.kwargs['club_id']
        club = Club.objects.get(id = club_id)
        try:
            role = Role.objects.get(user = self.request.user, club = club,role = 'CO') 
        except ObjectDoesNotExist:
            return redirect('feed')
        else:
            if role.role == 'CO':
                return render(self.request, 'club_templates/delete_club.html', {'club': club})


# @login_required
# def delete_club_action(request, club_id):
#     current_user = request.user
#     club = Club.objects.get(id = club_id)
#     try:
#         role = Role.objects.get(user = current_user, club = club)
#     except ObjectDoesNotExist:
#         return redirect('feed')
#     else:
#         if role.role == 'CO':
#             Club.objects.get(id = club_id).delete()
#             messages.add_message(request, messages.SUCCESS, "Club deleted! Time to make another one?")

#         return redirect('feed')


class DeleteClubActionView(LoginRequiredMixin,View):

    def get(self,*args, **kwargs):
        club_id = self.kwargs['club_id']
        current_user = self.request.user
        club = Club.objects.get(id = club_id)
        try:
            role = Role.objects.get(user = current_user, club = club)
        except ObjectDoesNotExist:
                return redirect('feed')
        else:
            if role.role == 'CO':
                    Club.objects.get(id = club_id).delete()
                    messages.add_message(self.request, messages.SUCCESS, "Club deleted! Time to make another one?")

            return redirect('feed')
    


    def post(self,request,*args, **kwargs):
       pass
        


class EditProfileView(LoginRequiredMixin, View):
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
        return render(request, 'user_templates/edit_profile.html', {'form': form, 'user': current_user})

    def render(self):
        current_user = self.request.user
        form = EditProfileForm(instance=current_user)
        return render(self.request,'user_templates/edit_profile.html', {'form': form})


"""Includes the view for a user's wishlist."""
class WishlistView(LoginRequiredMixin, ListView):

    def get(self, request, user_id):
        return self.render(user_id)

    def render(self, user_id):
        try:
            user = User.objects.get(id = user_id)
            return render(self.request, 'user_templates/wishlist.html', {'user': user})

        except ObjectDoesNotExist:
            return redirect('feed')


"""This function allows the club owner of the club to
    promote the member to the officer"""
# def promote_member_to_officer(request, club_id, member_id):
#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             user = request.user
#             club = Club.objects.get(id = club_id)
#             userrole = Role.objects.filter(user=user,club=club)
#             redirect_url = reverse('club_members', kwargs={'club_id':club_id})
#             member = User.objects.get(id = member_id)
#             newOfficer = Role.objects.get(club = club, user = member)
#             newOfficer.role = 'O'
#             newOfficer.save()
#             members = [member for member in Role.objects.filter(club=club)]
#             return redirect(redirect_url,members = members,
#                                                 userrole = userrole,
#                                                 club = club)
#         else:
#             return redirect('login')
#     else:
#         return HttpResponseForbidden()


"""This function allows the club owner of the club to
    promote the member to the officer"""

class PromoteToOfficer(LoginRequiredMixin,View):
     
    def post(self,*args, **kwargs):
        club_id = self.kwargs['club_id']
        member_id = self.kwargs['member_id']
        user = self.request.user
        club = Club.objects.get(id = club_id)
        userrole = Role.objects.filter(user=user,club=club)
        redirect_url = reverse('club_members', kwargs={'club_id':club_id})
        member = User.objects.get(id = member_id)
        newOfficer = Role.objects.get(club = club, user = member)
        newOfficer.role = 'O'
        newOfficer.save()
        members = [member for member in Role.objects.filter(club=club)]
        return redirect(redirect_url,members = members,
                                                userrole = userrole,
                                                club = club)
        

    def get(self,*args, **kwargs):
        return HttpResponseForbidden()




"""This function allows the club owner of the club to
    promote the officer to the club owner, and the club
    owner will be the officer of the club"""
# def promote_officer_to_ClubOwner(request, club_id, member_id):
#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             user = request.user
#             club = Club.objects.get(id = club_id)
#             userrole = Role.objects.get(club=club,user=user)
#             redirect_url = reverse('club_members', kwargs={'club_id':club_id})
#             member = User.objects.get(id = member_id)
#             newClubOwner = Role.objects.get(club = club, user = member)
#             userrole.role = 'O'
#             userrole.save()
#             newClubOwner.role = 'CO'
#             newClubOwner.save()
#             members = [member for member in Role.objects.filter(club=club)]
#             return redirect(redirect_url,members = members,
#                                                 userrole = userrole,
#                                                 club = club)
#         else:
#             return redirect('login')
#     else:
#         return HttpResponseForbidden()

class PromoteToOwner(LoginRequiredMixin,View):
     
    def post(self,*args, **kwargs):
        club_id = self.kwargs['club_id']
        member_id = self.kwargs['member_id']

        user = self.request.user
        club = Club.objects.get(id = club_id)
        userrole = Role.objects.get(club=club,user=user)
        redirect_url = reverse('club_members', kwargs={'club_id':club_id})
        member = User.objects.get(id = member_id)
        newClubOwner = Role.objects.get(club = club, user = member)
        userrole.role = 'O'
        userrole.save()
        newClubOwner.role = 'CO'
        newClubOwner.save()
        members = [member for member in Role.objects.filter(club=club)]
        return redirect(redirect_url,members = members,
                                                userrole = userrole,
                                                club = club)
        

    def get(self,*args, **kwargs):
        return HttpResponseForbidden()

"""This function allows the club owner of the club to
    demote the officer to the member"""
# def demote_officer_to_member(request, club_id, member_id):
#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             user = request.user
#             userrole = Role.objects.filter(user=user)
#             redirect_url = reverse('club_members', kwargs={'club_id':club_id})
#             club = Club.objects.get(id = club_id)
#             member = User.objects.get(id = member_id)
#             newMember = Role.objects.get(club = club, user = member)
#             isOwner = Role.objects.get(club=club,user=request.user,role = 'CO')
#             newMember.role = 'M'
#             newMember.save()
#             members = [member for member in Role.objects.filter(club=club)]
#             return redirect(redirect_url,members = members,
#                                                 userrole = userrole,
#                                                 club = club)
#         else:
#             return redirect('login')
#     else:
#         return HttpResponseForbidden()


class DemoteOfficerView(LoginRequiredMixin,View):
     
    def post(self,*args, **kwargs):
        club_id = self.kwargs['club_id']
        member_id = self.kwargs['member_id']
        user = self.request.user
        userrole = Role.objects.filter(user=user)
        redirect_url = reverse('club_members', kwargs={'club_id':club_id})
        club = Club.objects.get(id = club_id)
        member = User.objects.get(id = member_id)
        newMember = Role.objects.get(club = club, user = member)
        isOwner = Role.objects.get(club=club,user=self.request.user,role = 'CO')
        newMember.role = 'M'
        newMember.save()
        members = [member for member in Role.objects.filter(club=club)]
        return redirect(redirect_url,members = members,
                                                userrole = userrole,
                                                club = club)
        

    def get(self,*args, **kwargs):
        return HttpResponseForbidden()

"""This function allows the club owner of the club to
    remove the member of the club"""
# def remove_member(request, club_id, member_id):
#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             user = request.user
#             userrole = Role.objects.filter(user=user)
#             redirect_url = reverse('club_members', kwargs={'club_id':club_id})
#             club = Club.objects.get(id = club_id)
#             member = User.objects.get(id = member_id)
#             newMember = Role.objects.get(club = club, user = member)
#             newMember.delete()
#             members = Role.objects.filter(club=club)
#             return redirect(redirect_url,members = members,
#                                                 userrole = userrole,
#                                                 club = club)
#         else:
#             return redirect('login')
#     else:
#         return HttpResponseForbidden()

class RemoveMemberView(LoginRequiredMixin,View):
     
    def post(self,*args, **kwargs):
        club_id = self.kwargs['club_id']
        member_id = self.kwargs['member_id']
        user = self.request.user
        userrole = Role.objects.filter(user=user)
        redirect_url = reverse('club_members', kwargs={'club_id':club_id})
        club = Club.objects.get(id = club_id)
        member = User.objects.get(id = member_id)
        newMember = Role.objects.get(club = club, user = member)
        newMember.delete()
        members = Role.objects.filter(club=club)
        return redirect(redirect_url,members = members,
                                                userrole = userrole,
                                                club = club)
        

    def get(self,*args, **kwargs):
        return HttpResponseForbidden()


"""This function allows the member of the club to
    leave the club, which means the role has been
    deleted"""
# @login_required
# def leave_club(request, club_id):
#     if request.method == 'POST':
#             user = request.user
#             current_club = Club.objects.get(id=club_id)
#             userrole = Role.objects.filter(club=current_club).get(user=user)
#             if userrole.role == "CO":
#                 messages.add_message(request, messages.INFO, f'You cannot leave a club that you own!')
#             else:
#                 redirect_url = reverse('club_members', kwargs={'club_id':club_id})
#                 members = Role.objects.filter(club=current_club)
#                 userrole.delete()
#                 post = MembershipPost.objects.create(user = user, club = current_club)
#                 post.join = False
#                 post.save()
#                 messages.add_message(request, messages.SUCCESS, f'You have successfully left {current_club.name}!')
#             return redirect('feed')
#     else:
#         return HttpResponseForbidden()


class LeaveClubView(LoginRequiredMixin,View):
    def post(self,request,*args, **kwargs):
        club_id = self.kwargs['club_id']
        user = self.request.user
        current_club = Club.objects.get(id=club_id)
        userrole = Role.objects.filter(club=current_club).get(user=user)
        if userrole.role == "CO":
            messages.add_message(request, messages.INFO, f'You cannot leave a club that you own!')
            return redirect('feed')
        else:
            redirect_url = reverse('club_members', kwargs={'club_id':club_id})
            members = Role.objects.filter(club=current_club)
            userrole.delete()
            post = MembershipPost.objects.create(user = user, club = current_club)
            post.join = False
            post.save()
            messages.add_message(request, messages.SUCCESS, f'You have successfully left {current_club.name}!')
            return redirect('feed')

    def get(self,request,*args, **kwargs):
        return HttpResponseForbidden()
        


# """This function allows the club owner of the club to
#     accept the application the applicant, it means
#     the applicant will be the member of the club"""
# def accept_applicant_to_club_as_Owner(request,club_id,member_id):
#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             user = request.user
#             userrole = Role.objects.filter(user=user)
#             redirect_url = reverse('club_members', kwargs={'club_id':club_id})
#             club = Club.objects.get(id = club_id)
#             member = User.objects.get(id = member_id)
#             newMember = Role.objects.get(club = club, user = member)
#             newMember.role = 'M'
#             newMember.save()
#             MembershipPost.objects.create(user = member, club = club)
#             members = Role.objects.filter(club=club)
#             return redirect(redirect_url,members = members,
#                                                 userrole = userrole,
#                                                 club = club)
#         else:
#             return redirect('login')
#     else:
#         return HttpResponseForbidden()

class OwnerAcceptApplicantView(LoginRequiredMixin,View):
    def post(self,request,*args, **kwargs):
        club_id = self.kwargs['club_id']
        member_id = self.kwargs['member_id']
        user = self.request.user
        userrole = Role.objects.filter(user=user)
        redirect_url = reverse('club_members', kwargs={'club_id':club_id})
        club = Club.objects.get(id = club_id)
        member = User.objects.get(id = member_id)
        newMember = Role.objects.get(club = club, user = member)
        newMember.role = 'M'
        newMember.save()
        MembershipPost.objects.create(user = member, club = club)
        members = Role.objects.filter(club=club)
        return redirect(redirect_url,members = members,
                                                userrole = userrole,
                                                club = club)        

    def get(self,request,*args, **kwargs):
        return HttpResponseForbidden()

"""This function allows the officer of the club to
    accept the application the applicant, it means
    the applicant will be the member of the club"""
# def accept_applicant_to_club_as_officer(request,club_id,member_id):
#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             user = request.user
#             userrole = Role.objects.filter(user=user)
#             redirect_url = reverse('club_members', kwargs={'club_id':club_id})
#             club = Club.objects.get(id = club_id)
#             member = User.objects.get(id = member_id)
#             newMember = Role.objects.get(club = club, user = member)
#             newMember.role = 'M'
#             newMember.save()
#             MembershipPost.objects.create(user = member, club = club)
#             members = Role.objects.filter(club=club)
#             return redirect(redirect_url,members = members,
#                                                 userrole = userrole,
#                                                 club = club)
#         return redirect('login')
#     else:
#         return HttpResponseForbidden()

class OfficerApplicantAccept(LoginRequiredMixin,View):

    def get(self,*args, **kwargs):
        return HttpResponseForbidden()

    def post(self,*args, **kwargs):
            club_id = self.kwargs['club_id']
            member_id = self.kwargs['member_id']
            user = self.request.user
            userrole = Role.objects.filter(user=user)
            redirect_url = reverse('club_members', kwargs={'club_id':club_id})
            club = Club.objects.get(id = club_id)
            member = User.objects.get(id = member_id)
            newMember = Role.objects.get(club = club, user = member)
            newMember.role = 'M'
            newMember.save()
            MembershipPost.objects.create(user = member, club = club)
            members = Role.objects.filter(club=club)
            return redirect(redirect_url,members = members,
                                                userrole = userrole,
                                                club = club)
    


"""This function allows the club owner of the club to
    reject the application the applicant, it means
    the applicant will be removed from the club"""
# def reject_applicant_to_club_as_Owner(request,club_id,member_id):
#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             user = request.user
#             userrole = Role.objects.filter(user=user)
#             redirect_url = reverse('club_members', kwargs={'club_id':club_id})
#             club = Club.objects.get(id = club_id)
#             member = User.objects.get(id = member_id)
#             newMember = Role.objects.get(club = club, user = member)
#             newMember.delete()
#             members = Role.objects.filter(club=club)
#             return redirect(redirect_url,members = members,
#                                                 userrole = userrole,
#                                                 club = club)
#         else:
#             return redirect('login')
#     else:
#         return HttpResponseForbidden()

class OwnerApplicantRejectView(LoginRequiredMixin,View):

    def get(self,*args, **kwargs):
        return HttpResponseForbidden()

    def post(self,*args, **kwargs):
            club_id = self.kwargs['club_id']
            member_id = self.kwargs['member_id']
            user = self.request.user
            userrole = Role.objects.filter(user=user)
            redirect_url = reverse('club_members', kwargs={'club_id':club_id})
            club = Club.objects.get(id = club_id)
            member = User.objects.get(id = member_id)
            newMember = Role.objects.get(club = club, user = member)
            newMember.delete()
            members = Role.objects.filter(club=club)
            return redirect(redirect_url,members = members,
                                                userrole = userrole,
                                                club = club)
    

"""This function allows the officer of the club to
    reject the application the applicant, it means
    the applicant will be removed from the club"""
# def reject_applicant_to_club_as_Officer(request,club_id,member_id):
#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             user = request.user
#             userrole = Role.objects.filter(user=user)
#             redirect_url = reverse('club_members', kwargs={'club_id':club_id})
#             club = Club.objects.get(id = club_id)
#             member = User.objects.get(id = member_id)
#             newMember = Role.objects.get(club = club, user = member)
#             newMember.delete()
#             members = Role.objects.filter(club=club)
#             return redirect(redirect_url,members = members,
#                                                 userrole = userrole,
#                                                 club = club)
#         else:
#             return redirect('login')
#     else:
#         return HttpResponseForbidden()

class OfficerApplicantRejectView(LoginRequiredMixin,View):

    def get(self,*args, **kwargs):
        return HttpResponseForbidden()

    def post(self,*args, **kwargs):
            club_id = self.kwargs['club_id']
            member_id = self.kwargs['member_id']
            user = self.request.user
            userrole = Role.objects.filter(user=user)
            redirect_url = reverse('club_members', kwargs={'club_id':club_id})
            club = Club.objects.get(id = club_id)
            member = User.objects.get(id = member_id)
            newMember = Role.objects.get(club = club, user = member)
            newMember.delete()
            members = Role.objects.filter(club=club)
            return redirect(redirect_url,members = members,
                                                userrole = userrole,
                                                club = club)

"""This function returns the member list of the club,
    if the user does not belong to the club or the user
    is the applicant of the club does not have the
    authority to view the list.
    Otherwise, the user will see the list of the members of the club
    And the member can not see the details of the members
    only officers and club owners can do this"""

# class InvitationlistView(LoginRequiredMixin, ListView):

#     def get(self, request, user_id):
#         return self.render(user_id)

#     def render(self, user_id):
#         try:
#             user = User.objects.get(id = user_id)
#             invitations = Invitation.objects.filter(user=user, status="P")
#             return render(self.request, 'invitation_list.html', {'invitations': invitations})

#         except ObjectDoesNotExist:
#             return redirect('feed')



# @login_required
# def club_members(request, club_id):
#     club = Club.objects.get(id=club_id)
#     members = Role.objects.filter(club=club)
#     try:
#         userrole = Role.objects.get(club = club, user=request.user)
#     except ObjectDoesNotExist:
#         messages.add_message(request,messages.ERROR,"It seem you don't belong to this club!")
#         return redirect('club_list')
#     else:
#         if userrole.role == "A":
#             messages.add_message(request,messages.ERROR,"You are the applicant in this club, so you don't have authority to view the member list!")
#             return redirect('club_list')
#         else:
#             return render(request, 'club_templates/club_page.html', {'members': members,
#                                                     'userrole': userrole,
#                                                     'club' : club})

class ClubMembersView(LoginRequiredMixin,ListView):
    def get(self,request,*args, **kwargs):
        return self.render()

    
    # def get_queryset(self):
    #     club_id = self.kwargs['club_id']
    #     QuerySet =  super().get_queryset()
    #     club = Club.objects.get(id=club_id)
    #     members = Role.objects.filter(club=club)
    #     QuerySet = members
    

    def render(self,*args, **kwargs):
        club_id = self.kwargs['club_id']
        club = Club.objects.get(id=club_id)
        members = Role.objects.filter(club=club)
        try:
            userrole = Role.objects.get(club = club, user=self.request.user)
        except ObjectDoesNotExist:
            messages.add_message(self.request,messages.ERROR,"It seem you don't belong to this club!")
            return redirect('club_list')
        else:
            if userrole.role == "A":
                messages.add_message(self.request,messages.ERROR,"You are the applicant in this club, so you don't have authority to view the member list!")
                return redirect('club_list')
            else:
                return render(self.request, 'club_templates/club_page.html', {'members': members,
                                                        'userrole': userrole,
                                                        'club' : club})


# @login_required
# def apply(request, club_id):
#     current_club = Club.objects.get(id=club_id)
#     if request.method == "POST":
#         if request.user.is_authenticated:
#             current_user = request.user
#             try:
#                 role = Role.objects.filter(club=current_club).get(user=current_user)
#             except ObjectDoesNotExist:
#                 messages.add_message(request,messages.SUCCESS,"You applied to this club successfully")
#                 role = Role.objects.create(user=current_user, club=current_club, role='A')
#                 return redirect('club_list')
#             else:
#                 messages.add_message(request,messages.ERROR,"You've already applied for this club!")
#                 return redirect('feed')
#         else:
#             return redirect('login')
#     else:
#         return HttpResponseForbidden()

class ApplyView(LoginRequiredMixin,View):

    def get(self,*args, **kwargs):
        return HttpResponseForbidden()

    def post(self,request,club_id):
        return self.render()
        
    


    def render(self,*args, **kwargs):
        club_id = self.kwargs['club_id']
        current_club = Club.objects.get(id=club_id)
        try:
            role = Role.objects.filter(club=current_club).get(user=self.request.user)
        except ObjectDoesNotExist:
            messages.add_message(self.request,messages.SUCCESS,"You applied to this club successfully")
            role = Role.objects.create(user=self.request.user, club=current_club, role='A')
            return redirect('club_list')
        else:
            messages.add_message(self.request,messages.ERROR,"You've already applied for this club!")
            return redirect('feed')


"""These functions are for adding/removing
     books from a user's wishlist."""
# @login_required
# def wish(request, book_id):
#     user = request.user
#     try:
#         book = Book.objects.get(pk = book_id)
#         if user.wishlist.filter(isbn=book.isbn).exists() == False:
#             user.wishlist.add(book)
#         return redirect('show_book', book.id)

#     except ObjectDoesNotExist:
#         return redirect('book_list')


class WishView(LoginRequiredMixin,View):


    def get(self,*args, **kwargs):
        return self.render()

    def post(self,*args, **kwargs):
        return self.render()
    


    def render(self,*args, **kwargs):
        user = self.request.user
        book_id = self.kwargs['book_id']
        try:
            book = Book.objects.get(pk = book_id)
            if user.wishlist.filter(isbn=book.isbn).exists() == False:
                user.wishlist.add(book)
            return redirect('show_book', book.id)

        except ObjectDoesNotExist:
            return redirect('book_list')     

@login_required
def unwish(request, book_id):
    user = request.user
    try:
        book = Book.objects.get(pk = book_id)
        previous_url = request.META.get('HTTP_REFERER')
        if user.wishlist.filter(isbn=book.isbn).exists():
            user.wishlist.remove(book)
            if previous_url != None and 'wishlist' in previous_url:
                return redirect('wishlist', user.id)
        return redirect('show_book', book.id)

    except ObjectDoesNotExist:
        return redirect('book_list')

class UnwishView(LoginRequiredMixin,View):


    def get(self,*args, **kwargs):
        return self.render()

    def post(self,*args, **kwargs):
        return self.render()
    


    def render(self,*args, **kwargs):
        user = self.request.user
        book_id = self.kwargs['book_id']
        try:
            book = Book.objects.get(pk = book_id)
            previous_url = self.request.META.get('HTTP_REFERER')
            if user.wishlist.filter(isbn=book.isbn).exists():
                user.wishlist.remove(book)
                if previous_url != None and 'wishlist' in previous_url:
                    return redirect('wishlist', user.id)
            return redirect('show_book', book.id)

        except ObjectDoesNotExist:
            return redirect('book_list')

"""This function is for club owner/officer to set the book for
    club to read"""
@login_required
def set_club_book(request, club_id):
    current_user = request.user
    club = Club.objects.get(id=club_id)
    if request.method == 'POST':
        form = SetClubBookForm(request.POST)
        if form.is_valid():
            book = form.get_book()
            current_owned_club = Role.objects.filter(user=current_user, role='O', club=club) | \
                                 Role.objects.filter(user=current_user, role='CO', club=club)
            club_book = Club.objects.filter(club_book= book, id= club_id)
            if current_owned_club.count() == 1:
                if club_book.count() == 0:
                    club._add_book(book)
                    return redirect('club_feed', club.id)
                else:
                    messages.add_message(request, messages.ERROR, "this book has already added")
                    form = SetClubBookForm()
                    return redirect('set_club_book', club.id)
            else:
                messages.add_message(request, messages.ERROR, "you don't own this club")
                form = SetClubBookForm()
                return redirect('club_list')
        else:
            messages.add_message(request, messages.ERROR, "Invalid club name or book name")
            form = SetClubBookForm()
            return redirect('set_club_book', club.id)
    else:
        form = SetClubBookForm()
    return render(request, 'club_templates/set_club_book.html', {'form': form, 'club': club})


# class SetClubBookView(FormView):

#     form_class = SetClubBookForm
#     template_name = 'club_templates/set_club_book.html'

#     def form_valid(self,*args, **kwargs):
#             current_user = self.request.user
#             club_id = self.kwargs['club_id']
#             club = Club.objects.get(id=club_id)
#             book = form.get_book()
#             current_owned_club = Role.objects.filter(user=current_user, role='O', club=club) | \
#                                  Role.objects.filter(user=current_user, role='CO', club=club)
#             club_book = Club.objects.filter(club_book= book, id= club_id)
#             if current_owned_club.count() == 1:
#                 if club_book.count() == 0:
#                     club._add_book(book)
#                     return redirect('club_feed', club.id)
#                 else:
#                     messages.add_message(self.request, messages.ERROR, "this book has already added")
#                     return redirect('set_club_book', club.id)
#             else:
#                 messages.add_message(self.request, messages.ERROR, "you don't own this club")
#                 return redirect('club_list')

#     def form_invalid(self,*args, **kwargs):
#         club_id = self.kwargs['club_id']
#         club = Club.objects.get(id=club_id)
#         messages.add_message(self.request, messages.ERROR, "Invalid club name or book name")
#         return redirect('set_club_book', club.id)




"""This function allows club office/owner to
    invite other users to join the club"""
@login_required
def invite(request, club_id):
    current_user = request.user
    club = Club.objects.get(id=club_id)
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            owned_club = Role.objects.filter(user=current_user, role='O', club=club) |\
                                 Role.objects.filter(user=current_user, role='CO', club=club)
            invited = Invitation.objects.filter(user=user, club=club, status='P')
            isMember = Role.objects.filter(club=club, user=user)
            if owned_club.count() == 1:
                if invited.count() == 0 and isMember.count() == 0:
                    invitations = Invitation.objects.create(user=user, club=club, status='P')
                    return redirect('club_members', club.id)
                else:
                    messages.add_message(request, messages.ERROR, "you have already invited this user "
                                                                  "or this user already in the club")
                    form = InviteForm()
                    return redirect('invite', club.id)
            else:
                messages.add_message(request, messages.ERROR, "you don't have the permission to invite others")
                form = InviteForm()
                return redirect('club_list')
        else:
            messages.add_message(request, messages.ERROR, "Invalid username")
            form = InviteForm()
            return redirect('invite', club.id)
    else:
        form = InviteForm()
    return render(request, 'club_templates/invite.html', {'form': form, 'club':club})



# class InviteView(FormView):

#     form_class = InviteForm
#     template_name = 'club_templates/invite.html'


#     def form_valid(self,form,*args, **kwargs):
#             club_id = self.kwargs['club_id']
#             current_user = self.request.user
#             club = club = Club.objects.get(id=club_id)
#             user = form.get_user()
#             owned_club = Role.objects.filter(user=current_user, role='O', club=club) |\
#                                  Role.objects.filter(user=current_user, role='CO', club=club)
#             invited = Invitation.objects.filter(user=user, club=club, status='P')
#             isMember = Role.objects.filter(club=club, user=user)
#             if owned_club.count() == 1:
#                 if invited.count() == 0 and isMember.count() == 0:
#                     invitations = Invitation.objects.create(user=user, club=club, status='P')
#                     return redirect('club_members', club.id)
#                 else:
#                     messages.add_message(self.request, messages.ERROR, "you have already invited this user "
#                                                                   "or this user already in the club")
#                     form = InviteForm()
#                     return redirect('invite', club.id)
#             else:
#                 messages.add_message(self.request, messages.ERROR, "you don't have the permission to invite others")
#                 form = InviteForm()
#                 return redirect('club_list')

        

#     def form_invalid(self,*args, **kwargs):
#         club_id = self.kwargs['club_id']
#         club = Club.objects.get(id=club_id)
#         messages.add_message(self.request, messages.ERROR, "Invalid username")
#         form = InviteForm()
#         return redirect('invite', club.id)



"""This function allows users to accept the invitation from the club"""
# def accept_invitation(request, inv_id):
#     if request.method == "POST":
#         user = request.user
#         invitation = Invitation.objects.get(id=inv_id)
#         club = invitation.club
#         new_role = Role.objects.create(user=user, club=club, role="M")
#         MembershipPost.objects.create(user = user, club = club)
#         old_invitation = Invitation.objects.filter(id=inv_id).delete()
#         messages.add_message(request, messages.INFO, "join successful")
#         return redirect('invitation_list', user.id)
#     else:
#         return HttpResponseForbidden()

class AcceptInvitationView(View):

    def post(self,request,inv_id):
        user = self.request.user
        invitation = Invitation.objects.get(id=inv_id)
        club = invitation.club
        new_role = Role.objects.create(user=user, club=club, role="M")
        MembershipPost.objects.create(user = user, club = club)
        old_invitation = Invitation.objects.filter(id=inv_id).delete()
        messages.add_message(request, messages.INFO, "join successful")
        return redirect('invitation_list', user.id)

    def get(self,request):
        return HttpResponseForbidden()


"""This function allows users to reject the invitation from the club"""
# def reject_invitation(request, inv_id):
#     if request.method == "POST":
#         user = request.user
#         invitation = Invitation.objects.get(id=inv_id)
#         club = invitation.club
#         old_invitation = Invitation.objects.filter(id=inv_id).delete()
#         messages.add_message(request, messages.INFO, "you have rejected this invitation")
#         return redirect('invitation_list', user.id)
#     else:
#         return HttpResponseForbidden()

class RejectInvitationView(View):

    def post(self,request,inv_id):
        user = self.request.user
        invitation = Invitation.objects.get(id=inv_id)
        club = invitation.club
        old_invitation = Invitation.objects.filter(id=inv_id).delete()
        messages.add_message(request, messages.INFO, "you have rejected this invitation")
        return redirect('invitation_list', user.id)

    def get(self):
        return HttpResponseForbidden()


"""This view class allows users to see all the pending invitation from the club"""
class InvitationlistView(LoginRequiredMixin, ListView):

    def get(self, request, user_id):
        return self.render(user_id)

    def render(self, user_id):
        try:
            user = User.objects.get(id = user_id)
            invitations = Invitation.objects.filter(user=user, status="P")
            return render(self.request, 'invitation_list.html', {'invitations': invitations})

        except ObjectDoesNotExist:
            return redirect('feed')

# @login_required
# def club_feed(request,club_id):
#     user=request.user
#     form = UserPostForm()
#     comment_form = CommentForm
#     club = Club.objects.get(id=club_id)
#     members = Role.objects.filter(club=club)
#     try:
#         userrole = Role.objects.get(club = club, user=request.user)
#     except ObjectDoesNotExist:
#         messages.add_message(request, messages.ERROR, "It seems you don't belong to this club!")
#         return redirect('club_list')
#     else:
#         if userrole.role == "A":
#             messages.add_message(request, messages.ERROR, "You are an applicant in this club, you don't have authority to view the member list!")
#             return redirect('club_list')
#         else:
#             event_posts = EventPost.objects.filter(event__club=club)
#             comments = Comment.objects.filter(club=club)
#             membership_posts = MembershipPost.objects.filter(club=club)
#             user_posts = UserPost.objects.filter(club=club)
#             posts = sorted( chain(event_posts, membership_posts, user_posts),
#                     key=lambda instance: instance.created_at,reverse=True)
#             return render(request, 'club_templates/club_feed.html', {'members': members,
#                                                        'userrole': userrole,
#                                                        'posts':posts,
#                                                        'club' : club,
#                                                        'form' : form,
#                                                        'comment_form' : comment_form,
#                                                        'comments' : comments,
#                                                        'user':user})


class ClubFeedView(LoginRequiredMixin,View):

    def get(self,*args, **kwargs):
        return self.render()

    def post(self,request,club_id):
        self.render()
        
    


    def render(self,*args, **kwargs):
            club_id = self.kwargs['club_id']
            user=self.request.user
            form = UserPostForm()
            comment_form = CommentForm
            club = Club.objects.get(id=club_id)
            members = Role.objects.filter(club=club)
            try:
                userrole = Role.objects.get(club = club, user=self.request.user)
            except ObjectDoesNotExist:
                messages.add_message(self.request, messages.ERROR, "It seems you don't belong to this club!")
                return redirect('club_list')
            else:
                if userrole.role == "A":
                    messages.add_message(self.request, messages.ERROR, "You are an applicant in this club, you don't have authority to view the member list!")
                    return redirect('club_list')
                else:
                    event_posts = EventPost.objects.filter(event__club=club)
                    comments = Comment.objects.filter(club=club)
                    membership_posts = MembershipPost.objects.filter(club=club)
                    user_posts = UserPost.objects.filter(club=club)
                    posts = sorted( chain(event_posts, membership_posts, user_posts),
                            key=lambda instance: instance.created_at,reverse=True)
                    return render(self.request, 'club_templates/club_feed.html', {'members': members,
                                                            'userrole': userrole,
                                                            'posts':posts,
                                                            'club' : club,
                                                            'form' : form,
                                                            'comment_form' : comment_form,
                                                            'comments' : comments,
                                                            'user':user})



# def create_event(request, club_id):
#     club = Club.objects.get(id=club_id)
#     members = Role.objects.filter(club=club)
#     userrole = Role.objects.get(club = club, user=request.user)
#     events = Event.objects.filter(club = club)
#     if request.method == 'POST':
#         form = EventForm(request.POST)
#         current_user = request.user
#         if form.is_valid():
#             this_event = form.save(club_id,current_user)
#             EventPost.objects.create(event = this_event, user=request.user)
#             return redirect('events_list',club_id)
#         else:
#             messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
#     form = EventForm()
#     return render(request, 'club_templates/create_event.html', {'form': form,
#                                                  'members': members,
#                                                   'userrole': userrole,
#                                                   'club': club})

    
class CreateEventView(CreateView):

    def get(self,request,*args, **kwargs):
        return self.render()

    def form_valid(self,request,club_id):
        form = EventForm(request.POST)
        current_user = request.user
  
        this_event = form.save(club_id,current_user)
        EventPost.objects.create(event = this_event, user=request.user)
        return redirect('events_list',club_id)

    def form_invalid(self):
        messages.add_message(self.request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()


 

    def render(self,*args, **kwargs):
        club_id = self.kwargs['club_id']
        club = Club.objects.get(id=club_id)
        members = Role.objects.filter(club=club)
        userrole = Role.objects.get(club = club, user=self.request.user)
        events = Event.objects.filter(club = club)
        form = EventForm()
        return render(self.request, 'club_templates/create_event.html', {'form': form,
                                                    'members': members,
                                                    'userrole':userrole,
                                                    'club': club})





# def event_list(request,club_id):
#     club = Club.objects.get(id=club_id)
#     members = Role.objects.filter(club=club)
#     userrole = Role.objects.get(club = club, user=request.user)
#     try:
#         events = Event.objects.filter(club=club)
#     except ObjectDoesNotExist:
#         messages.add_message(request,messages.ERROR,"There are no events")
#         return redirect('club_list')
#     else:
#           return render(request, 'club_templates/events_list.html', {'members': members,
#                                                       'userrole': userrole,
#                                                       'club' : club,
#                                                       'events' : events})

class EventList(View):

    def get(self,*args, **kwargs):
        return self.render()

    def post(self,request,club_id):
        self.render()

    def render(self,*args, **kwargs):
        club_id = self.kwargs['club_id']
        club = Club.objects.get(id=club_id)
        members = Role.objects.filter(club=club)
        userrole = Role.objects.get(club = club, user=self.request.user)
        try:
            events = Event.objects.filter(club=club)
        except ObjectDoesNotExist:
            messages.add_message(self.request,messages.ERROR,"There are no events")
            return redirect('club_list')
        else:
            return render(self.request, 'club_templates/events_list.html', {'members': members,
                                                        'userrole': userrole,
                                                        'club' : club,
                                                        'events' : events})


class NewPostView(LoginRequiredMixin, CreateView):
    """Class-based generic view for new post handling."""

    model = UserPost
    template_name = 'club_templates/club_feed.html'
    form_class = UserPostForm
    http_method_names = ['post']

    def form_valid(self, form):
        """Process a valid form."""
        form.instance.author = self.request.user
        form.instance.club = Club.objects.get(id=(self.kwargs['club_id']))
        return super().form_valid(form)

    def get_success_url(self):
        """Return URL to redirect the user too after valid form handling."""

        return reverse('club_feed',kwargs={'club_id':self.kwargs['club_id']})

    def handle_no_permission(self):
        return redirect('login')

# @login_required
# def like_post(request, club_id, post_id):
#     try:
#         post = UserPost.objects.get(id=post_id)
#         if post.likes.filter(id=request.user.id).exists():
#             post.likes.remove(request.user)
#         else:

#             post.likes.add(request.user)
#     except ObjectDoesNotExist:
#         return HttpResponseRedirect(reverse('club_feed',kwargs={'club_id':club_id}))
#     else:
#         return HttpResponseRedirect(reverse('club_feed',kwargs={'club_id':club_id}))


class LikePostView(LoginRequiredMixin,View):

    def get(self,*args, **kwargs):
        return self.render()

    def post(self,request,club_id):
        self.render()
        
    def render(self,*args, **kwargs):
        post_id = self.kwargs['post_id']
        club_id = self.kwargs['club_id']
        try:
            post = UserPost.objects.get(id=post_id)
            if post.likes.filter(id=self.request.user.id).exists():
                post.likes.remove(self.request.user)
            else:

                post.likes.add(self.request.user)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('club_feed',kwargs={'club_id':club_id}))
        else:
            return HttpResponseRedirect(reverse('club_feed',kwargs={'club_id':club_id}))



@login_required
def add_comment_to_post(request, club_id, post_id):
    post = UserPost.objects.get(id=post_id)
    club = Club.objects.get(id=club_id)
    if request.method == "POST":
        comment = Comment.objects.create(club=club,post=post,user=request.user)
        form = CommentForm(request.POST, instance = comment)
        if form.is_valid():
            comment = form.save()
    return HttpResponseRedirect(reverse('club_feed',kwargs={'club_id':club_id}))

# class CommentOnPostView(LoginRequiredMixin,FormView):
    
#     form_class = CommentForm
    
#     def form_valid(self, form,*args, **kwargs):
#         club_id = self.kwargs['club_id']
#         post_id = self.kwargs['post_id']
#         post = UserPost.objects.get(id=post_id)
#         club = Club.objects.get(id=club_id)
#         self.object = Comment.objects.create(club=club,post=post,user=self.request.user)
#         self.object = form.save()
    
#     def form_invalid(self, form,*args, **kwargs):
#         club_id = self.kwargs['club_id']
#         return HttpResponseRedirect(reverse('club_feed',kwargs={'club_id':club_id}))

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, user, month, year):
        roles = Role.objects.filter(user=user)
        events_per_day = []
        for role in roles:
            events_per_day+=(Event.objects.filter(deadline__day=day,club=role.club, deadline__month=month, deadline__year = year))

        d = ''
        for event in events_per_day:
            d += f'<li> {event.name} </li>'

        if day != 0:
            if not events_per_day :
                return f"<td><span class='date'>{day}</span></td>"
            else:
                return f"<td><mark style='background-color:#ced4da'>{day}</mark></td>"

        return '<td></td>'

    def formatweek(self, theweek, user, month, year):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, user, month, year)
        return f'<tr> {week} </tr>'

    def formatmonth(self, user, withyear=True):
        user=user
        month=self.month
        year=self.year

        cal = f'<table>\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, user, month, year)}\n'
        cal += f'</table>\n'
        return cal


class CalendarView(LoginRequiredMixin,generic.ListView):
    model = Event
    template_name = 'user_templates/profile.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)


        user=self.request.user

        roles = Role.objects.filter(user=user)
        events= []
        for role in roles:
            events+=(Event.objects.filter(club=role.club, deadline__month=d.month, deadline__year =d.year))

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True, user=user)
        context['calendar'] = mark_safe(html_cal)
        context['events'] = events
        context['user'] = user

        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.today()

def join_event(request,event_id,club_id):
     club = Club.objects.get(id=club_id)
     members = Role.objects.filter(club=club)
     userrole = Role.objects.get(club = club, user=request.user)
     event = Event.objects.get(id=event_id)
     event.save()
     event.join_event(request.user)
     events = Event.objects.filter(club = club)
     return render(request, 'club_templates/events_list.html', {'members': members,
                                                   'userrole': userrole,
                                                   'club' : club,
                                                   'events' : events})

def add_user_to_interested_list(request,event_id,club_id):
     club = Club.objects.get(id=club_id)
     members = Role.objects.filter(club=club)
     userrole = Role.objects.get(club = club, user=request.user)
     event = Event.objects.get(id=event_id)
     event.add_user_to_interested_field(request.user)
     events = Event.objects.filter(club = club)
     return render(request, 'club_templates/events_list.html', {'members': members,
                                                   'userrole': userrole,
                                                   'club' : club,
                                                   'events' : events})
def event_page(request,event_id,club_id):
     club = Club.objects.get(id=club_id)
     event = Event.objects.get(id=event_id)
     return render(request, 'club_templates/event_page.html', {'event': event,
                                                               'club' : club})
def join_event_from_event_page(request,event_id,club_id):
    club = Club.objects.get(id=club_id)
    event = Event.objects.get(id=event_id)
    event.join_event(request.user)
    return render(request, 'club_templates/event_page.html', {'event': event,
                                                              'club' : club})

def add_user_to_interested_list_from_event_page(request,event_id,club_id):
    club = Club.objects.get(id=club_id)
    event = Event.objects.get(id=event_id)
    event.add_user_to_interested_field(request.user)
    return render(request, 'club_templates/event_page.html', {'event': event,
                                                              'club' : club})


def user_chat(request, receiver_id):
    user = request.user
    receiver = User.objects.get(id=receiver_id)
    return render(request, 'user_templates/user_chat.html', {
        'user':user,
        'receiver':receiver
    })


def send_user_message(request):
    user = request.user
    if request.method == "POST":
        text = request.POST.get('text')
        user_id = user.id
        receiver_id = request.POST.get('receiver_id')
        user = User.objects.get(id=user_id)
        receiver = User.objects.get(id=receiver_id)
        new_message = Message.objects.create(text=text, user=user, receiver=receiver)
        new_message.save()
        return render(request, 'user_templates/user_chat.html')
    else:
        return HttpResponseForbidden()


class SendUserMessageView(View):

    def get(self,*args, **kwargs):
        return HttpResponseForbidden()


    def post(self,*args, **kwargs):
        user = self.request.user
        text = self.request.POST.get('text')
        user_id = user.id
        receiver_id = self.request.POST.get('receiver_id')
        user = User.objects.get(id=user_id)
        receiver = User.objects.get(id=receiver_id)
        new_message = Message.objects.create(text=text, user=user, receiver=receiver)
        new_message.save()
        return render(self.request, 'user_templates/user_chat.html')
    


def get_user_messages(request, receiver_id):
    user = request.user
    receiver = User.objects.get(id=receiver_id)
    messages = Message.objects.filter(user=user, receiver=receiver) | \
               Message.objects.filter(user=receiver, receiver=user)
    order_messages = messages.order_by("id")
    message_list = []
    for message in order_messages:
        message_list.append({
            "username": message.get_username(),
            "text":message.text
            })

    return JsonResponse({"messages":message_list})


def club_chat(request, club_id):
    user = request.user
    club = Club.objects.get(id=club_id)
    return render(request, 'club_templates/club_chat.html', {
        'user': user,
        'club': club
    })


# def send_club_message(request):
#     if request.method == "POST":
#         text = request.POST.get('text')
#         user_id = request.POST.get('user_id')
#         club_id = request.POST.get('club_id')
#         user = User.objects.get(id=user_id)
#         club = Club.objects.get(id=club_id)
#         try:
#             role = Role.objects.get(user=user, club=club)
#             if role.role == "O" or role.role == "CO" or role.role == "M":
#                 new_message = Message.objects.create(text=text, user=user, club=club)
#                 new_message.save()
#                 return render(request, 'club_templates/club_chat.html')
#             else:
#                 return redirect('club_list')
#         except ObjectDoesNotExist:
#             return HttpResponseForbidden()
#     else:
#         return HttpResponseForbidden()


class SendClubMessage(LoginRequiredMixin,View):

    def get(self,*args, **kwargs):
       return HttpResponseForbidden()

    def post(self,request,*args, **kwargs):
        club_id = self.request.POST.get('club_id')
        user_id = self.request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        club = Club.objects.get(id=club_id)
        text = self.request.POST.get('text')
        try:
            role = Role.objects.get(user=user, club=club)
            if role.role == "O" or role.role == "CO" or role.role == "M":
                new_message = Message.objects.create(text=text, user=user, club=club)
                new_message.save()
                return render(self.request, 'club_templates/club_chat.html')
            else:
                return redirect('club_list')
        except ObjectDoesNotExist:
            return HttpResponseForbidden()
        

       


def get_club_messages(request, club_id):
    club = Club.objects.get(id=club_id)
    messages = Message.objects.filter(club=club)
    message_list = []
    for message in messages:
        message_list.append({
            "username": message.get_username(),
            "text":message.text
            })

    return JsonResponse({"messages":message_list})


class SearchView(ListView):
    template_name = 'search_view.html'
    count = 0
    query = ' '

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['search_form'] = SearchForm(initial={
            'search' : self.request.GET.get('search',''),
            'filter_field' : self.request.GET.get('filter_field', ''),
        })
        context['query'] = self.query
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')

        if query is not None:
            queryset = []
            book_results= Book.objects.search(query)
            club_results= Club.objects.search(query)
            user_results= User.objects.search(query)

            if filter_field == 'books':
                queryset = book_results
            elif filter_field == 'clubs':
                queryset =  club_results
            elif filter_field == 'users':
                queryset = user_results
            elif filter_field == 'all':
                queryset = chain(
                    book_results,
                    club_results,
                    user_results
                    )

            qs_sorted = sorted(queryset,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs_sorted)
            self.query = query
            return qs_sorted
        return query
