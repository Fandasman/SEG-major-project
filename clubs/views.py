from django import template
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from typing import List
from .club_list import ClubList
from .forms import SignUpForm, LogInForm, EditProfileForm, CreateClubForm
from .models import Club, User


# Create your views here.
#
def feed(request):
    current_user = request.user
    return render(request, 'feed.html', {'user': current_user})

# class FeedView(LoginRequiredMixin, ListView):
#     """Class-based generic view for displaying a view."""
#
#     model = User
#     template_name = "feed.html"
#     context_object_name = 'users'
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


# new implementation !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def getClubAndListOfClubsWithObjectParameter(obj):
    list_of_clubs = ClubList()
    name_of_club = obj.request.session.get('name')
    club = list_of_clubs.find_club(name_of_club)
    return club, list_of_clubs

def getClubAndListOfClubs(request):
    list_of_clubs = ClubList()
    name_of_club = request.session.get('name')
    club = list_of_clubs.find_club(name_of_club)
    return club, list_of_clubs

def club_selection(request):
    list_of_clubs = ClubList()
    clubs = list_of_clubs.club_list
    owners = []
    member_count_list = []
    for club in clubs:
        #owners.append(club.get_club_owner())
        member_count_list.append(User.objects.filter(groups__name__in = [club.getClubOwnerGroup(), club.getClubMemberGroup()]).count())
    clubs_and_owners = zip(clubs, owners, member_count_list)
    return render(request, 'club_selection.html', {'clubs_and_owners' : clubs_and_owners, 'clubs':clubs})


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
    #paginate_by = settings.USERS_PER_PAGE

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

class OwnerView(OwnerMemberListView):

    template_name = 'owner.html'

    def render(self):
        club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
        clubs = list_of_clubs.club_list
        users = User.objects.all()
        number_of_applicants = User.objects.filter(groups__name = club.getClubApplicantGroup()).count()
        number_of_members = User.objects.filter(groups__name__in = [ club.getClubOwnerGroup(), club.getClubMemberGroup()]).count()
        return render(self.request, 'owner.html', {'users': users, 'number_of_applicants': number_of_applicants, 'number_of_members': number_of_members, 'clubs': clubs})

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
