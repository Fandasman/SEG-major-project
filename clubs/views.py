from django import template
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView
from typing import List
from .club_list import ClubList
from .models import Book, Club, User


# Create your views here.

def feed(request):
    current_user = request.user
    return render(request, 'feed.html', {'user': current_user})

class LoginProhibitedMixin:

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('club_selection')

        return super().dispatch(*args, **kwargs)

class HomeView(LoginProhibitedMixin,View):
    template_name = 'home.html'

    def get(self,request):
        return self.render()

    def post(self,request):
        return self.render()

    def render(self):
        return render(self.request, 'home.html')
# # @login_required
# def show_book(request, book_id):
#     try:
#         book = Book.objects.get(id=book_id)
#     except ObjectDoesNotExist:
#         return redirect('search_books')
#     else:
#         return render(request, 'show_book.html',
#             {'book': book}
#         )
#
# # @login_required
# def show_club(request, club_id):
#     try:
#         club = Club.objects.get(id=club_id)
#     except ObjectDoesNotExist:
#         return redirect('search_clubs')
#     else:
#         return render(request, 'show_club.html',
#             {'club': club}
#         )
#
# # @login_required
# def show_user(request, user_id):
#     try:
#         user = User.objects.get(id=user_id)
#     except ObjectDoesNotExist:
#         return redirect('search_users')
#     else:
#         return render(request, 'show_user.html',
#             {'user': user}
#         )
#
# # @login_required
# def search_books(request):
#     search_book = request.GET.get('book_searchbar')
#     if search_book:
#         books= Book.objects.filter(Q(name__icontains=search_book))
#     else:
#         books = Book.objects.all()
#     return render(request, 'search_books.html', {'books': books})
#
# # @login_required
# def search_clubs(request):
#     search_club = request.GET.get('club_searchbar')
#     if search_club:
#         clubs= Club.objects.filter(Q(name__icontains=search_club))
#     else:
#         clubs = Club.objects.all()
#     return render(request, 'search_clubs.html', {'clubs': clubs})
#
# # @login_required
# def search_users(request):
#     search_user = request.GET.get('user_searchbar')
#     if search_user:
#         users= User.objects.filter(Q(username__icontains=search_user))
#     else:
#         users= User.objects.all()
#     return render(request, 'search_users.html', {'users': users})




# new implementation !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def getClubAndListOfClubsWithObjectParameter(obj):
    list_of_clubs = ClubList()
    name_of_club = obj.request.session.get('club_name')
    club = list_of_clubs.find_club(name_of_club)
    return club, list_of_clubs

def getClubAndListOfClubs(request):
    list_of_clubs = ClubList()
    name_of_club = request.session.get('club_name')
    club = list_of_clubs.find_club(name_of_club)
    return club, list_of_clubs

def club_selection(request):
    list_of_clubs = ClubList()
    clubs = list_of_clubs.club_list
    owners = []
    member_count_list = []
    for club in clubs:
        owners.append(club.get_club_owner())
        member_count_list.append(User.objects.filter(groups__name__in = [club.getClubOwnerGroup(), club.getClubMemberGroup()]).count())
    clubs_and_owners = zip(clubs, owners, member_count_list)
    return render(request, 'club_selection.html', {'clubs_and_owners' : clubs_and_owners, 'clubs':clubs})

class MemberOnlyMixin:

    def dispatch(self, *args, **kwargs):
        current_user = self.request.user
        club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
        if not (current_user.groups.filter(name = club.getClubMemberGroup()).exists() or current_user.groups.filter(name = club.getClubOwnerGroup()).exists()):
            return redirect('profile')
        return super().dispatch(*args, **kwargs)

class OwnerOnlyMixin:

    def dispatch(self, *args, **kwargs):
        current_user = self.request.user
        club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
        if not (current_user.groups.filter(name = club.getClubOwnerGroup()).exists()):
            return redirect('profile')
        return super().dispatch(*args, **kwargs)

class MemberListView(LoginRequiredMixin,MemberOnlyMixin,ListView):
    model = User
    template_name = 'member_list.html'
    context_object_name = 'users'

    def get_queryset(self):
          qs = super().get_queryset()
          club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
          return qs.filter(groups__name__in=[club.getClubApplicantGroup(), club.getClubOwnerGroup(), club.getClubMemberGroup()])

    def get(self,request,*args, **kwargs):
        return self.render()

    def post(self,request,*args, **kwargs):
        return self.redirect('club_selection')

    def render(self):
        qs = super().get_queryset()
        club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
        clubs = list_of_clubs.club_list
        users = qs.filter(groups__name__in=[club.getClubMemberGroup()])
        return render(self.request, 'member_list.html', {'users':users, 'clubs':clubs})

class OwnerMemberListView(OwnerOnlyMixin,MemberListView):
    template_name = 'owner_member_list.html'
    context_object_name = 'users'
    paginate_by = settings.USERS_PER_PAGE

    def get_context_data(self, *args, **kwargs):
        """Generate content to be displayed in the template."""
        context = super().get_context_data(*args, **kwargs)
        club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
        context['number_of_applicants'] = User.objects.filter(groups__name = club.getClubApplicantGroup()).count()
        context['number_of_members'] = User.objects.filter(groups__name__in = [club.getClubOwnerGroup(),club.getClubMemberGroup()]).count()
        return context

    def get(self,request,*args, **kwargs):
        return self.render()


    def post(self,request,*args, **kwargs):
        return self.render()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def render(self):
        qs = super().get_queryset()
        club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
        clubs = list_of_clubs.club_list
        users = qs.filter(groups__name__in=[club.getClubMemberGroup()])
        return render(self.request, 'owner_member_list.html', {'users':users, 'clubs':clubs})

class ShowUserView(DetailView):
    model = User
    template_name = 'show_user.html'
    pk_url_kwarg = "user_id"
