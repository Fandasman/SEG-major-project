from django import template
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from .forms import SignUpForm, LogInForm, EditProfileForm, ClubForm, SetClubBookForm, InviteForm
from .models import Book, Club, Role, User, Invitation, BooksRatings
from collections import Counter


# Create your views here.

def feed(request):
    current_user = request.user
    isbns = list(BooksRatings.objects.all().values_list('isbn'))

    sorted = [rating for ratings, c in Counter(isbns).most_common()
              for rating in [ratings] * c]

    ratings = list(dict.fromkeys(sorted))[:50]

    books = []

    for rating in ratings:
        book = Book.objects.get(isbn = rating[0])
        books.append(book)
    
    

    return render(request, 'feed.html', {'user': current_user, 'favourites': books})

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
        books= Book.objects.filter(name__icontains=search_book)
    else:
        books = Book.objects.all()
    return render(request, 'search_books.html', {'books': books})


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
        current_owned_clubs = Role.objects.filter(user = current_user, role = 'CO')
        if len(current_owned_clubs) < 3:
            form = ClubForm(request.POST)
            if form.is_valid():
                newClub = form.save()
                role = Role.objects.create(user = current_user, club = newClub, role = 'CO')
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


"""This function allows the club owner of the club to
    promote the member to the officer"""
def promote_member_to_officer(request, club_id, member_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            club = Club.objects.get(id = club_id)
            userrole = Role.objects.get(club=club,user=user)
            redirect_url = reverse('member_list', kwargs={'club_id':club_id})
            member = User.objects.get(id = member_id)
            newOfficer = Role.objects.get(club = club, user = member)
            isOwner = Role.objects.get(club=club,user=request.user,role = 'CO')
            newOfficer.role = 'O'
            newOfficer.save()
            members = [member for member in Role.objects.filter(club=club)]
            return redirect(redirect_url,members = members,
                                                userrole = userrole,
                                                club = club)
        else:
            return redirect('log_in')
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
            userrole = Role.objects.get(club=club,user=user)
            redirect_url = reverse('member_list', kwargs={'club_id':club_id})
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
            return redirect('log_in')
    else:
        return HttpResponseForbidden()

"""This function allows the club owner of the club to
    demote the officer to the member"""
def demote_officer_to_member(request, club_id, member_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            userrole = Role.objects.filter(user=user)
            redirect_url = reverse('member_list', kwargs={'club_id':club_id})
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
            return redirect('log_in')
    else:
        return HttpResponseForbidden()

"""This function allows the club owner of the club to
    remove the member of the club"""
def remove_member(request, club_id, member_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            userrole = Role.objects.filter(user=user)
            redirect_url = reverse('member_list', kwargs={'club_id':club_id})
            club = Club.objects.get(id = club_id)
            member = User.objects.get(id = member_id)
            newMember = Role.objects.get(club = club, user = member)
            newMember.delete()
            members = Role.objects.filter(club=club)
            return redirect(redirect_url,members = members,
                                                userrole = userrole,
                                                club = club)
        else:
            return redirect('log_in')
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
            redirect_url = reverse('member_list', kwargs={'club_id':club_id})
            members = Role.objects.filter(club=current_club)
            userrole.delete()
            return redirect('user_details')
        else:
            return redirect('log_in')
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
            redirect_url = reverse('member_list', kwargs={'club_id':club_id})
            club = Club.objects.get(id = club_id)
            member = User.objects.get(id = member_id)
            newMember = Role.objects.get(club = club, user = member)
            newMember.role = 'M'
            newMember.save()
            members = Role.objects.filter(club=club)
            return redirect(redirect_url,members = members,
                                                userrole = userrole,
                                                club = club)
        else:
            return redirect('log_in')
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
            redirect_url = reverse('member_list', kwargs={'club_id':club_id})
            club = Club.objects.get(id = club_id)
            member = User.objects.get(id = member_id)
            newMember = Role.objects.get(club = club, user = member)
            newMember.role = 'M'
            newMember.save()
            members = Role.objects.filter(club=club)
            return redirect(redirect_url,members = members,
                                                userrole = userrole,
                                                club = club)
        return redirect('log_in')
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
            redirect_url = reverse('member_list', kwargs={'club_id':club_id})
            club = Club.objects.get(id = club_id)
            member = User.objects.get(id = member_id)
            newMember = Role.objects.get(club = club, user = member)
            newMember.delete()
            members = Role.objects.filter(club=club)
            return redirect(redirect_url,members = members,
                                                userrole = userrole,
                                                club = club)
        else:
            return redirect('log_in')
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
            redirect_url = reverse('member_list', kwargs={'club_id':club_id})
            club = Club.objects.get(id = club_id)
            member = User.objects.get(id = member_id)
            newMember = Role.objects.get(club = club, user = member)
            newMember.delete()
            members = Role.objects.filter(club=club)
            return redirect(redirect_url,members = members,
                                                userrole = userrole,
                                                club = club)
        else:
            return redirect('log_in')
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
def member_list(request, club_id):
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
            return render(request, 'club_page.html', {'members': members,
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
            return redirect('log_in')
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
        return redirect('search_books')

def unwish(request, book_id):
    user = request.user
    try:
        book = Book.objects.get(pk = book_id)
        if user.wishlist.filter(isbn=book.isbn).exists():
            user.wishlist.remove(book)
        return redirect('wishlist', user.id)
    
    except ObjectDoesNotExist:
        return redirect('search_books')


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
                    return redirect('show_club', club.id)
                else:
                    messages.add_message(request, messages.ERROR, "this book has already added")
                    form = SetClubBookForm()
                    return redirect('set_club_book', club.id)
            else:
                messages.add_message(request, messages.ERROR, "you don't own this club")
                form = SetClubBookForm()
                return redirect('show_club', club.id)
        else:
            messages.add_message(request, messages.ERROR, "Invalid club name or book name")
            form = SetClubBookForm()
            return redirect('set_club_book', club.id)
    else:
        form = SetClubBookForm()
    return render(request, 'set_club_book.html', {'form': form, 'club': club})


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
                    return redirect('show_club', club.id)
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
    return render(request, 'invite.html', {'form': form, 'club':club})


"""This function allows users to accept the invitation from the club"""
def accept_invitation(request, inv_id):
    if request.method == "POST":
        user = request.user
        invitation = Invitation.objects.get(id=inv_id)
        club = invitation.club
        new_role = Role.objects.create(user=user, club=club, role="M")
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
