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
from unicodedata import name
from os import name
from django.contrib import admin
from django.urls import path
from clubs import views
from django.conf.urls import url

urlpatterns = [

    path('feed/', views.CalendarView.as_view(),name="feed"),
    path('add_comment/<int:club_id>/<int:post_id>', views.add_comment_to_post,name = "add_comment"),
    path('all_members/<int:club_id>/', views.club_members, name = "club_members"),
    path('club_feed/<int:club_id>/', views.club_feed, name = "club_feed"),
    path('club_event_creation/<int:club_id>/', views.create_event,name = "create_event"),
    path('club_events_list/<int:club_id>/',views.event_list,name = "events_list"),
    path('join_event/<int:club_id>/<int:event_id>/',views.join_event,name="join_event"),
    path('interested_in_event/<int:club_id>/<int:event_id>/',views.add_user_to_interested_list,name="interested_in_event"),
    path('join_event_event_page/<int:club_id>/<int:event_id>/',views.join_event_from_event_page,name="join_event_from_event_page"),
    path('interested_in_event_event_page/<int:club_id>/<int:event_id>/',views.add_user_to_interested_list_from_event_page,name="interested_in_event_from_event_page"),
    path('event_page/<int:club_id>/<int:event_id>/',views.event_page,name="event_page"),
    path('leave_club/<int:club_id>/',views.leave_club,name = "leave_club"),
    path('admin/', admin.site.urls),
    path('add_book/<int:club_id>/',views.ClubBookView.as_view(), name='add_book'),
    path('', views.HomeView.as_view(), name = 'home'),
    path('club_list', views.ClubListView.as_view(), name = 'club_list'),
    path('club/<int:club_id>', views.ShowClubView.as_view(), name='show_club'),
    path('feed/', views.feed, name='feed'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('like_post/<int:club_id>/<int:post_id>', views.like_post, name='like_post'),
    path('new_post/<int:club_id>/', views.NewPostView.as_view(), name='new_post'),
    #path('feed/', views.feed, name='feed'),
    path('profile/', views.profile, name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('logout/', views.log_out, name='log_out'),
    path('create_club/', views.create_club, name ='create_club'),
    path('user/<int:user_id>/wishlist', views.WishlistView.as_view(), name = 'wishlist'),
    path('log_in/', views.LogInView.as_view(), name='login'),
    path('member_club_list', views.MemberClubListView.as_view(), name = 'member_club_list'),
    path('user_list', views.UserListView.as_view(), name = 'user_list'),
    path('owner_club_list', views.OwnerClubListView.as_view(), name = 'owner_club_list'),
    path('recommended_club_list', views.RecommendedClubListView.as_view(), name = 'recommended_club_list'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
<<<<<<< HEAD
    path('book/<int:book_id>', views.ShowBookView.as_view(), name='show_book'),
=======
    path('select_genres/', views.select_genres, name='select_genres'),
    path('book/<int:book_id>', views.show_book, name='show_book'),
    path('remove_rating/<int:book_id>', views.remove_rating, name='remove_rating'),
>>>>>>> 67c3ad16c9244813f45d373463c1cd385c351512
    path('user/<int:user_id>', views.ShowUserView.as_view(), name='show_user'),
    path('club/<int:club_id>', views.ShowClubView.as_view(), name='show_club'),
    path('promoted/<int:club_id>/<int:member_id>', views.promote_member_to_officer, name = "promotion"),
    path('promote/<int:club_id>/<int:member_id>', views.promote_officer_to_ClubOwner, name = "promotionOfficer"),
    path('demoted/<int:club_id>/<int:member_id>', views.demote_officer_to_member, name = "demotion"),
    path('removemember/<int:club_id>/<int:member_id>', views.remove_member, name = "removemember"),
    path('leave/<int:club_id>', views.leave_club, name = "leave_club"),
    path('accept_applicant/<int:club_id>/<int:member_id>', views.accept_applicant_to_club_as_Owner, name = "accept_applicant_as_owner"),
    path('accept_applicant_as_officer/<int:club_id>/<int:member_id>', views.accept_applicant_to_club_as_officer, name = "accept_applicant"),
    path('rejectAsOwner/<int:club_id>/<int:member_id>', views.reject_applicant_to_club_as_Owner, name = "rejectasowner"),
    path('rejectAsOfficer/<int:club_id>/<int:member_id>', views.reject_applicant_to_club_as_Officer, name = "rejectasofficer"),
    path('apply/<int:club_id>', views.apply, name='apply'),
    path('book_list/', views.BookListView.as_view(), name='book_list'),
    path('book/<int:book_id>/wish', views.wish, name='wish'),
    path('book/<int:book_id>/unwish', views.unwish, name='unwish'),
    path('club/<int:club_id>/set_club_book/', views.set_club_book, name = 'set_club_book'),
    path('club/<int:club_id>/invite/', views.invite, name='invite'),
    path('user/<int:user_id>/invitation_list/', views.InvitationlistView.as_view(), name='invitation_list'),
    path('accept_invitation/<int:inv_id>', views.accept_invitation, name='accept_invitation'),
    path('reject_invitation/<int:inv_id>', views.reject_invitation, name='reject_invitation'),
    path('club/<int:club_id>/chat/', views.club_chat, name='club_chat'),
    path('send_club_message/', views.send_club_message, name='send_club_message'),
    path('get_club_messages/<int:club_id>/', views.get_club_messages, name='get_club_messages'),
    path('user/<int:receiver_id>/chat/', views.user_chat, name='user_chat'),
    path('send_user_message/', views.send_user_message, name='send_user_message'),
    path('get_user_messages/<int:receiver_id>/', views.get_user_messages, name='get_user_messages'),
    path('search_view/', views.SearchView.as_view(), name='search_view')
]
