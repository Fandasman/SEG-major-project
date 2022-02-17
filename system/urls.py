"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path
from clubs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name = 'home'),
    #path('create_club/', views.CreateClubView, name ='create_club'),
    path('club_list', views.ClubListView.as_view(), name = 'club_list'),
    path('club/<int:club_id>', views.ShowClubView.as_view(), name='show_club'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('feed/', views.feed, name='feed'),
    path('profile/', views.profile, name='profile'),
    #path('users/', views.search_users, name='search_users'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.log_out, name='log_out'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('create_club/', views.create_club, name ='create_club'),
    path('user/<int:user_id>/wishlist', views.WishlistView.as_view(), name = 'wishlist'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('member_club_list', views.MemberClubListView.as_view(), name = 'member_club_list'),
    path('member_list', views.MemberListView.as_view(), name = 'member_list'),
    path('owner_club_list', views.OwnerClubListView.as_view(), name = 'owner_club_list'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('book/<int:book_id>', views.show_book, name='show_book'),
    path('user/<int:user_id>', views.ShowUserView.as_view(), name='show_user'),
    path('search_books/', views.search_books, name='search_books'),
]
