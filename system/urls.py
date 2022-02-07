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
from django.contrib import admin
from django.urls import path
from clubs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('book/<int:book_id>', views.show_book, name='show_book'),
    path('books/', views.search_books, name='search_books'),
    path('club/<int:club_id>', views.show_club, name='show_club'),
    path('clubs/', views.search_clubs, name='search_clubs'),
    path('feed/', views.feed, name='feed'),
    path('user/<int:user_id>', views.show_user, name='show_user'),
    path('users/', views.search_users, name='search_users'),

]
