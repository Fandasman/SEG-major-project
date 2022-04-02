from django import template
from django.conf import settings
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from itertools import chain
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.http.response import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .forms import ClubBookForm, SignUpForm, LogInForm, EditProfileForm, ClubForm
from django.conf import settings
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from .models import Book, Club, Role, User, Invitation

from .forms import SignUpForm, LogInForm, EditProfileForm, ClubForm, SetClubBookForm, InviteForm, EventForm
from .models import Book, Club, Role, User, Invitation, Message,Event

from .forms import SignUpForm, LogInForm, EditProfileForm, ClubForm, SetClubBookForm, InviteForm,EventForm, UserPostForm, CommentForm, SearchForm
from .models import Book, Club, Role, User, Invitation, Event, EventPost, UserPost, MembershipPost, Comment
from itertools import chain
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import generic
from django.utils.safestring import mark_safe
import calendar
from calendar import HTMLCalendar
import csv
from django.http import StreamingHttpResponse


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
def profile(request):
    current_user = request.user
    return render(request, 'user_templates/profile.html',
            {'user': current_user}
        )

<<<<<<< HEAD
# @login_required
def search_books(request):
    search_book = request.GET.get('book_searchbar')
    if search_book:
        books= Book.objects.filter(name__icontains=search_book)
    else:
        books = Book.objects.all()
    return render(request, 'book_templates/search_books.html', {'books': books})


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

class HomeView(View):
    template_name = 'main_templates/home.html'

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
        context= super().get_context_data(*args, **kwargs)
        club= Club.objects.all()
        context['roles']= Role.objects.all().filter(role= "O")
        return context

class OwnerClubListView(LoginRequiredMixin, ListView):
    model= Club
    template_name= 'club_templates/owner_club_list.html'
    context_object_name= 'clubs'
    paginate_by = settings.CLUBS_PER_PAGE
    ordering = ['name']

    def get_context_data(self, *args, **kwargs):
        context= super().get_context_data(*args, **kwargs)
        current_user= self.request.user
        context['roles']= Role.objects.all().filter(user= current_user, role= "CO")
        return context

class MemberClubListView(LoginRequiredMixin, ListView):
    model= Club
    template_name= 'club_templates/member_club_list.html'
    context_object_name= 'clubs'
    paginate_by = settings.CLUBS_PER_PAGE
    ordering = ['name']

    def get_context_data(self, *args, **kwargs):
        context= super().get_context_data(*args, **kwargs)
        current_user= self.request.user
        context['roles']= Role.objects.all().filter(user= current_user, role= "M")
        return context

class ShowBookView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'book_templates/show_book.html'
    pk_url_kwarg = "book_id"

    def get(self, request, *args, **kwargs):
        try:
            return super().get(self, request, *args, **kwargs)
        except Http404:
            return redirect('book_list')

class ShowUserView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user_templates/show_user.html'
    pk_url_kwarg = "user_id"

    def get(self, request, *args, **kwargs):
        try:
            return super().get(self, request, *args, **kwargs)
        except Http404:
            return redirect('user_list')

class ShowClubView(LoginRequiredMixin, DetailView):
    model = Club
    template_name = 'club_templates/show_club.html'
    pk_url_kwarg = "club_id"

    def get(self, request, *args, **kwargs):
        try:
            return super().get(self, request, *args, **kwargs)
        except Http404:
            return redirect('club_list')


class LogInView(View):
    """Log-in handling view"""
    def get(self,request):
        return self.render()

    def post(self,request):
        form = LogInForm(request.POST)
        user = form.get_user()
        if user is not None:
                """Redirect to club selection page, with option to create new club"""
                login(request, user)
                return redirect('feed')

        else:
            messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
            return self.render()
            
    def render(self):
        form = LogInForm()
        return render(self.request, 'login.html', {'form': form})

"""View used for logging out."""
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
    template_name = "main_templates/sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    template_name = "sign_up.html"
    #redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN


    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)

"""This function standardize the requirements for
    creating clubs, if club is successfully created,
    it will be store in the database and client will
    be redirected to the feed page"""
@login_required
def create_club(request):
    current_user = request.user
    if request.method == 'POST':
        current_user = request.user
        current_owned_clubs = Role.objects.filter(user = current_user, role = 'CO')
        if len(current_owned_clubs) < 3:
            form = ClubForm(request.POST)
            if form.is_valid():
                newClub = form.save()
                MembershipPost.objects.create(club = newClub, user = current_user)
                role = Role.objects.create(user = current_user, club = newClub, role = 'CO')
                return redirect('club_list')
        else:
            messages.add_message(request, messages.ERROR, "You already own too many clubs!")
            form = ClubForm()
        return render(request, 'club_templates/create_club.html' , {'form': form})

    else:
        form = ClubForm()
        return render(request, 'club_templates/create_club.html' , {'form': form})



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
        return render(request, 'user_templates/edit_profile.html', {'form': form, 'user': current_user})

    def render(self):
        current_user = self.request.user
        form = EditProfileForm(instance=current_user)
        return render(self.request,'user_templates/edit_profile.html', {'form': form})



class ClubBookView(View):
    def get(self,club_id,request):
        club = Club.objects.get(id=club_id)
        return self.render()

    def post(self,club_id,request):
    
        form = ClubBookForm(data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Book amended!")
            form.save()
            club = Club.objects.get(id=club_id)
            current_book = form.cleaned_data.get('current_book')
            book_page = form.cleaned_data.get('book_page')
            Club.objects.filter(club_book=current_book, id= club_id)
            Club.objects.filter(book_page=book_page, id= club_id)
            return redirect('feed')
        return render(request, 'club_book.html', {'form': form})


    def render(self):
        current_user = self.request.user
        form = ClubBookForm(instance=current_user)
        return render(self.request,'club_book.html', {'form': form})

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
def promote_member_to_officer(request, club_id, member_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
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
        else:
            return redirect('login')
    else:
        return HttpResponseForbidden()

"""This function allows the club owner of the club to
    promote the officer to the club owner, and the club
    owner will be the officer of the club"""
def promote_officer_to_ClubOwner(request, club_id, member_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
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
        else:
            return redirect('login')
    else:
        return HttpResponseForbidden()

"""This function allows the club owner of the club to
    demote the officer to the member"""
def demote_officer_to_member(request, club_id, member_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            userrole = Role.objects.filter(user=user)
            redirect_url = reverse('club_members', kwargs={'club_id':club_id})
            club = Club.objects.get(id = club_id)
            member = User.objects.get(id = member_id)
            newMember = Role.objects.get(club = club, user = member)
            isOwner = Role.objects.get(club=club,user=request.user,role = 'CO')
            newMember.role = 'M'
            newMember.save()
            members = [member for member in Role.objects.filter(club=club)]
            return redirect(redirect_url,members = members,
                                                userrole = userrole,
                                                club = club)
        else:
            return redirect('login')
    else:
        return HttpResponseForbidden()

"""This function allows the club owner of the club to
    remove the member of the club"""
def remove_member(request, club_id, member_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
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
        else:
            return redirect('login')
    else:
        return HttpResponseForbidden()

"""This function allows the member of the club to
    leave the club, which means the role has been
    deleted"""
def leave_club(request, club_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            current_club = Club.objects.get(id=club_id)
            userrole = Role.objects.filter(club=current_club).get(user=user)
            redirect_url = reverse('club_members', kwargs={'club_id':club_id})
            members = Role.objects.filter(club=current_club)
            userrole.delete()
            post = MembershipPost.objects.create(user = user, club = current_club)
            post.join = False
            post.save()
            return redirect('feed')
        else:
            return redirect('login')
    else:
        return HttpResponseForbidden()

"""This function allows the club owner of the club to
    accept the application the applicant, it means
    the applicant will be the member of the club"""
def accept_applicant_to_club_as_Owner(request,club_id,member_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
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
        else:
            return redirect('login')
    else:
        return HttpResponseForbidden()

"""This function allows the officer of the club to
    accept the application the applicant, it means
    the applicant will be the member of the club"""
def accept_applicant_to_club_as_officer(request,club_id,member_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
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
        return redirect('login')
    else:
        return HttpResponseForbidden()


"""This function allows the club owner of the club to
    reject the application the applicant, it means
    the applicant will be removed from the club"""
def reject_applicant_to_club_as_Owner(request,club_id,member_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            userrole = Role.objects.filter(user=user)
            redirect_url = reverse('club_members', kwargs={'club_id':club_id})
            club = Club.objects.get(id = club_id)
            member = User.objects.get(id = member_id)
            newMember = Role.objects.get(club = club, user = member)
            # print(Role.objects.filter(club=club).count())
            newMember.delete()
            members = Role.objects.filter(club=club)
            return redirect(redirect_url,members = members,
                                                userrole = userrole,
                                                club = club)
        else:
            return redirect('login')
    else:
        return HttpResponseForbidden()

"""This function allows the officer of the club to
    reject the application the applicant, it means
    the applicant will be removed from the club"""
def reject_applicant_to_club_as_Officer(request,club_id,member_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
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
        else:
            return redirect('login')
    else:
        return HttpResponseForbidden()

"""This function returns the member list of the club,
    if the user does not belong to the club or the user
    is the applicant of the club does not have the
    authority to view the list.
    Otherwise, the user will see the list of the members of the club
    And the member can not see the details of the members
    only officers and club owners can do this"""
@login_required
def club_members(request, club_id):
    club = Club.objects.get(id=club_id)
    members = Role.objects.filter(club=club)
    try:
        userrole = Role.objects.get(club = club, user=request.user)
    except ObjectDoesNotExist:
        messages.add_message(request,messages.ERROR,"It seem you don't belong to this club!")
        return redirect('club_list')
    else:
        if userrole.role == "A":
            messages.add_message(request,messages.ERROR,"You are the applicant in this club, so you don't have authority to view the member list!")
            return redirect('club_list')
        else:
            return render(request, 'club_templates/club_page.html', {'members': members,
                                                    'userrole': userrole,
                                                    'club' : club})

"""This function is for the user to apply for the club.
    If the user already in the club, system will refuse
    to create a role for the user with an error message."""
def apply(request, club_id):
    current_club = Club.objects.get(id=club_id)
    if request.method == "POST":
        if request.user.is_authenticated:
            current_user = request.user
            try:
                role = Role.objects.filter(club=current_club).get(user=current_user)
            except ObjectDoesNotExist:
                messages.add_message(request,messages.SUCCESS,"You applied to this club successfully")
                role = Role.objects.create(user=current_user, club=current_club, role='A')
                return redirect('club_list')
            else:
                messages.add_message(request,messages.ERROR,"You've already applied for this club!")
                return redirect('feed')
        else:
            return redirect('login')
    else:
        return HttpResponseForbidden()

def wish(request, book_id):
    user = request.user
    try:
        book = Book.objects.get(pk = book_id)
        if user.wishlist.filter(isbn=book.isbn).exists() == False:
            user.wishlist.add(book)
        return redirect('show_book', book.id)

    except ObjectDoesNotExist:
        return redirect('book_list')

def unwish(request, book_id):
    user = request.user
    try:
        book = Book.objects.get(pk = book_id)
        if user.wishlist.filter(isbn=book.isbn).exists():
            user.wishlist.remove(book)
        return redirect('wishlist', user.id)

    except ObjectDoesNotExist:
        return redirect('book_list')


"""This function is for club owner/officer to set the book for
    club to read"""
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
                return redirect('club_feed', club.id)
        else:
            messages.add_message(request, messages.ERROR, "Invalid club name or book name")
            form = SetClubBookForm()
            return redirect('set_club_book', club.id)
    else:
        form = SetClubBookForm()
    return render(request, 'club_templates/set_club_book.html', {'form': form, 'club': club})


"""This function allows club office/owner to
    invite other users to join the club"""
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
                return redirect('show_club', club.id)
        else:
            messages.add_message(request, messages.ERROR, "Invalid username")
            form = InviteForm()
            return redirect('invite', club.id)
    else:
        form = InviteForm()
    return render(request, 'club_templates/invite.html', {'form': form, 'club':club})


"""This function allows users to accept the invitation from the club"""
def accept_invitation(request, inv_id):
    if request.method == "POST":
        user = request.user
        invitation = Invitation.objects.get(id=inv_id)
        club = invitation.club
        new_role = Role.objects.create(user=user, club=club, role="M")
        MembershipPost.objects.create(user = user, club = club)
        old_invitation = Invitation.objects.filter(id=inv_id).delete()
        messages.add_message(request, messages.INFO, "join successful")
        return redirect('invitation_list', user.id)
    else:
        return HttpResponseForbidden()




"""This function allows users to reject the invitation from the club"""
def reject_invitation(request, inv_id):
    if request.method == "POST":
        user = request.user
        invitation = Invitation.objects.get(id=inv_id)
        club = invitation.club
        old_invitation = Invitation.objects.filter(id=inv_id).delete()
        messages.add_message(request, messages.INFO, "you have rejected this invitation")
        return redirect('invitation_list', user.id)
    else:
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

def club_feed(request,club_id):
    user=request.user
    form = UserPostForm()
    comment_form = CommentForm
    club = Club.objects.get(id=club_id)
    members = Role.objects.filter(club=club)
    try:
        userrole = Role.objects.get(club = club, user=request.user)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "It seems you don't belong to this club!")
        return redirect('club_list')
    else:
        if userrole.role == "A":
            messages.add_message(request, messages.ERROR, "You are an applicant in this club, you don't have authority to view the member list!")
            return redirect('club_list')
        else:
            event_posts = EventPost.objects.filter(event__club=club)
            comments = Comment.objects.filter(club=club)
            membership_posts = MembershipPost.objects.filter(club=club)
            user_posts = UserPost.objects.filter(club=club)
            posts = sorted( chain(event_posts, membership_posts, user_posts),
                    key=lambda instance: instance.created_at,reverse=True)
            return render(request, 'club_templates/club_feed.html', {'members': members,
                                                       'userrole': userrole,
                                                       'posts':posts,
                                                       'club' : club,
                                                       'form' : form,
                                                       'comment_form' : comment_form,
                                                       'comments' : comments,
                                                       'user':user})



def create_event(request, club_id):
    club = Club.objects.get(id=club_id)
    members = Role.objects.filter(club=club)
    userrole = Role.objects.get(club = club, user=request.user)
    events = Event.objects.filter(club = club)
    if request.method == 'POST':
        form = EventForm(request.POST)
        current_user = request.user
        if form.is_valid():
            this_event = form.save(club_id,current_user)
            EventPost.objects.create(event = this_event, user=request.user)
            return redirect('events_list',club_id)
        else:
            messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = EventForm()
    return render(request, 'club_templates/create_event.html', {'form': form,
                                                 'members': members,
                                                  'userrole': userrole,
                                                  'club': club})
def event_list(request,club_id):
    club = Club.objects.get(id=club_id)
    members = Role.objects.filter(club=club)
    userrole = Role.objects.get(club = club, user=request.user)
    try:
        events = Event.objects.filter(club=club)
    except ObjectDoesNotExist:
        messages.add_message(request,messages.ERROR,"There are no events")
        return redirect('club_list')
    else:
          return render(request, 'club_templates/events_list.html', {'members': members,
                                                      'userrole': userrole,
                                                      'club' : club,
                                                      'events' : events})


class NewPostView(LoginRequiredMixin, CreateView):
    """Class-based generic view for new post handling."""

    model = UserPost
    template_name = 'club_feed.html'
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
        return redirect('log_in')

def like_post(request, club_id, post_id):
    post = UserPost.objects.get(id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:

        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('club_feed',kwargs={'club_id':club_id}))


def add_comment_to_post(request, club_id, post_id):
    post = UserPost.objects.get(id=post_id)
    club = Club.objects.get(id=club_id)
    if request.method == "POST":
        comment = Comment.objects.create(club=club,post=post,user=request.user)
        form = CommentForm(request.POST, instance = comment)
        if form.is_valid():
            comment = form.save()
    return HttpResponseRedirect(reverse('club_feed',kwargs={'club_id':club_id}))


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


class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendar.html'


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

        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
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

def leave_club(request,club_id):
    club = Club.objects.get(id = club_id)
    role = Role.objects.filter(club= club).get(user = request.user).delete()
    return redirect('feed')


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


def send_club_message(request):
    if request.method == "POST":
        text = request.POST.get('text')
        user_id = request.POST.get('user_id')
        club_id = request.POST.get('club_id')
        user = User.objects.get(id=user_id)
        club = Club.objects.get(id=club_id)
        try:
            role = Role.objects.get(user=user, club=club)
            if role.role == "O" or role.role == "CO" or role.role == "M":
                new_message = Message.objects.create(text=text, user=user, club=club)
                new_message.save()
                return render(request, 'club_templates/club_chat.html')
            else:
                return redirect('club_list')
        except ObjectDoesNotExist:
            return HttpResponseForbidden()
    else:
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

