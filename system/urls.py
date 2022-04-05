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

    # path('feed/', views.CalendarView.as_view(),name="feed"),
    path('add_comment/<int:club_id>/<int:post_id>', views.add_comment_to_post,name = "add_comment"),
    path('all_members/<int:club_id>/', views.ClubMembersView.as_view(), name = "club_members"),
    path('club_feed/<int:club_id>/', views.ClubFeedView.as_view(), name = "club_feed"),
    path('club_event_creation/<int:club_id>/', views.CreateEventView.as_view(),name = "create_event"),
    path('club_events_list/<int:club_id>/',views.EventList.as_view(),name = "events_list"),
    path('join_event/<int:club_id>/<int:event_id>/',views.JoinEventView.as_view(),name="join_event"),
    path('interested_in_event/<int:club_id>/<int:event_id>/',views.AddUsertoInterestedView.as_view(),name="interested_in_event"),
    path('join_event_event_page/<int:club_id>/<int:event_id>/',views.join_event_from_event_page,name="join_event_from_event_page"),
    path('interested_in_event_event_page/<int:club_id>/<int:event_id>/',views.add_user_to_interested_list_from_event_page,name="interested_in_event_from_event_page"),
    path('event_page/<int:club_id>/<int:event_id>/',views.event_page,name="event_page"),
    path('leave_club/<int:club_id>/',views.LeaveClubView.as_view(),name = "leave_club"),
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name = 'home'),
    path('club_list', views.ClubListView.as_view(), name = 'club_list'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('like_post/<int:club_id>/<int:post_id>', views.LikePostView.as_view(), name='like_post'),
    path('new_post/<int:club_id>/', views.NewPostView.as_view(), name='new_post'),
    path('feed/', views.feed, name='feed'),
    path('profile/', views.CalendarView.as_view(), name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('logout/', views.log_out, name='log_out'),
    path('create_club/', views.CreateClubView.as_view(), name ='create_club'),
    path('user/<int:user_id>/wishlist', views.WishlistView.as_view(), name = 'wishlist'),
    path('log_in/', views.LogInView.as_view(), name='login'),
    path('member_club_list', views.MemberClubListView.as_view(), name = 'member_club_list'),
    path('user_list', views.UserListView.as_view(), name = 'user_list'),
    path('owner_club_list', views.OwnerClubListView.as_view(), name = 'owner_club_list'),
    path('recommended_club_list', views.RecommendedClubListView.as_view(), name = 'recommended_club_list'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('select_genres/', views.SelectGenresView.as_view(), name='select_genres'),
    path('remove_rating/<int:book_id>', views.RemoveRatingView.as_view(), name='remove_rating'),
    path('book/<int:book_id>', views.show_book, name='show_book'),
    path('user/<int:user_id>', views.ShowUserView.as_view(), name='show_user'),
    path('club/<int:club_id>', views.ShowClubView.as_view(), name='show_club'),
    path('promoted/<int:club_id>/<int:member_id>', views.PromoteToOfficer.as_view(), name = "promotion"),
    path('promote/<int:club_id>/<int:member_id>', views.PromoteToOwner.as_view(), name = "promotionOfficer"),
    path('demoted/<int:club_id>/<int:member_id>', views.DemoteOfficerView.as_view(), name = "demotion"),
    path('removemember/<int:club_id>/<int:member_id>', views.RemoveMemberView.as_view(), name = "removemember"),
    path('leave/<int:club_id>', views.LeaveClubView.as_view(), name = "leave_club"),
    path('accept_applicant/<int:club_id>/<int:member_id>', views.OwnerAcceptApplicantView.as_view(), name = "accept_applicant_as_owner"),
    path('accept_applicant_as_officer/<int:club_id>/<int:member_id>', views.OfficerApplicantAccept.as_view(), name = "accept_applicant"),
    path('rejectAsOwner/<int:club_id>/<int:member_id>', views.OwnerApplicantRejectView.as_view(), name = "rejectasowner"),
    path('rejectAsOfficer/<int:club_id>/<int:member_id>', views.OfficerApplicantRejectView.as_view(), name = "rejectasofficer"),
    path('apply/<int:club_id>', views.ApplyView.as_view(), name='apply'),
    path('book_list/', views.BookListView.as_view(), name='book_list'),
    path('book/<int:book_id>/wish', views.WishView.as_view(), name='wish'),
    path('book/<int:book_id>/unwish', views.UnwishView.as_view(), name='unwish'),
    path('club/<int:club_id>/set_club_book/', views.set_club_book, name = 'set_club_book'),
    path('club/<int:club_id>/invite/', views.invite, name='invite'),
    path('user/<int:user_id>/invitation_list/', views.InvitationlistView.as_view(), name='invitation_list'),
    path('accept_invitation/<int:inv_id>', views.AcceptInvitationView.as_view(), name='accept_invitation'),
    path('reject_invitation/<int:inv_id>', views.RejectInvitationView.as_view(), name='reject_invitation'),
    path('club/<int:club_id>/chat/', views.club_chat, name='club_chat'),
    path('send_club_message/', views.SendClubMessage.as_view(), name='send_club_message'),
    path('get_club_messages/<int:club_id>/', views.get_club_messages, name='get_club_messages'),
    path('user/<int:receiver_id>/chat/', views.user_chat, name='user_chat'),
    path('send_user_message/', views.SendUserMessageView.as_view(), name='send_user_message'),
    path('get_user_messages/<int:receiver_id>/', views.get_user_messages, name='get_user_messages'),
    path('club/<int:club_id>/delete_club/', views.DeleteClubView.as_view(), name='delete_club'),
    path('club/<int:club_id>/delete/', views.DeleteClubActionView.as_view(), name='delete_club_action'),
    path('search_view/', views.SearchView.as_view(), name='search_view'),
]
