import datetime
from secrets import choice
from django.db import models
from django.db.models import Q
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager as AbstractUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from libgravatar import Gravatar
from multiselectfield import MultiSelectField
from .helpers import get_genres
from datetime import date
from datetime import timedelta
from .validators import validate_date
from django.urls import reverse

# Create the Book model

class UserAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Email must be set!')
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        return self.get(code_number=email_)


class BookManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(author__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct()
        return qs

class ClubManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            lookup = Q(name__icontains=query)
            qs = qs.filter(lookup).distinct()
        return qs


class UserManager(AbstractUserManager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(username__icontains=query) |
                         Q(first_name__icontains=query) |
                         Q(last_name__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct()
        return qs


class Book(models.Model):
    isbn = models.CharField(max_length = 13, unique = True, blank = False)
    title = models.CharField(max_length = 100, blank = False)
    author = models.CharField(max_length = 100, blank = False)
    publisher = models.CharField(max_length = 100, blank = False)
    published = models.IntegerField(
        default = datetime.datetime.now().year,
        validators = [MaxValueValidator(datetime.datetime.now().year), MinValueValidator(0)]
    )
    genre = models.CharField(max_length = 50, blank = False)
    imgURLSmall = models.URLField(blank = True)
    imgURLMedium = models.URLField(blank = True)
    imgURLLarge = models.URLField(blank = True)
    objects= BookManager()

    def get_absolute_url(self):
        return reverse('show_book', args=[str(self.id)])

    def get_title(self):
        return self.title


# Create the User model
class User(AbstractUser):
    username = models.CharField(
        max_length = 30,
        unique = True,
        validators = [
            RegexValidator(
                regex = r'^\w{3,}$',
                message = "The username must contain at least three characters!"
            )
        ]
    )

    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField(unique = True, blank = False)
    bio = models.CharField(max_length = 500, blank = True)
    wishlist = models.ManyToManyField(Book, related_name="wishlist", blank=True)
    genres_preferences = MultiSelectField(
        choices=get_genres(),
        max_choices=5,
        blank=True,
        default=None
    )
    objects= UserManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size = 120):
        g_object = Gravatar(self.email)
        url = g_object.get_image(size = size, default = 'mp')
        return url

    def mini_gravatar(self):
        return self.gravatar(size = 60)

    def get_wishlist(self):
          return "\n".join([b.wishlist for b in self.wishlist.all()])

    def get_current_user_role(self):
        return Role.objects.filter(user = self)

    def get_absolute_url(self):
        return reverse('show_user', args=[str(self.id)])


# Create the Books and Ratings model
class BooksRatings(models.Model):
    isbn = models.CharField(max_length = 13, blank = False)
    rating = models.IntegerField(
        choices = [(rating, rating) for rating in range(1,6)],
        validators = [MaxValueValidator(5), MinValueValidator(1)]
    )
    user = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('show_user', args=[str(self.id)])

    class Meta():
        unique_together = ('user', 'isbn',)

# Create the book Club model
class Club(models.Model):
    name = models.CharField(
        max_length = 50,
        unique = True,
        validators = [
            RegexValidator(
                regex = r'^.{3,}$',
                message = 'The name of the club must contain at least three characters!'
                )
        ]
    )
    location = models.CharField(max_length = 100, blank = False)
    description = models.CharField(max_length = 500, blank = False)
    club_book = models.ForeignKey(Book, related_name="club_book", blank = True, null = True, on_delete=models.CASCADE)
    objects= ClubManager()

    def _add_book(self, club):
        club.club_book.add(self)

    def get_club_officers(self):
      return Role.objects.filter(club = self).filter(role = "O")

    def get_club_owner(self):
        return Role.objects.filter(club = self).filter(role = "CO")

    def get_club_members(self):
        return Role.objects.filter(club = self).filter(role = "M")

    def get_all_aplicants(self):
        return Role.objects.filter(club = self).filter(role ="A")

    def get_all_administrators(self):
       return Role.objects.filter(club = self).filter(role = 'O' ).count() + 1

    def get_upcoming_events(self):
        return Event.objects.filter(deadline__gte = date.today())

    def get_past_events(self):
        start_date = datetime.date(2021, 3, 13)
        end_date = datetime.date.today() - timedelta(days = 1)
        return Event.objects.filter(deadline__range = (start_date,end_date))

    def get_absolute_url(self):
        return reverse('club_feed', args=[str(self.id)])


# Create the user's Roles model
ROLES = (
    ('A', 'Applicant'),
    ('M', 'Member'),
    ('O', 'Officer'),
    ('CO', 'Owner')
)

class Role(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=2,
        choices=ROLES,
        default='A'
    )

    def __str__(self):
        return self.user.full_name() + " is " + self.role

    def get_club_name(self):
        return self.club.name

    def get_role(self):
        return self.role
        
    class Meta():
        unique_together = ('user', 'club',)


# Create the Invitation model
STATUS = {
    ('P', 'Pending'),
    ('A', 'Accept'),
    ('R', 'Reject'),
}

class Invitation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default='P'
    )

    class Meta():
        unique_together = ('user', 'club',)

    def get_club_name(self):
        return self.club.name

# Create the Event model
class Event(models.Model):

    name = models.CharField(
        max_length = 50,
        blank=False,
        unique=True,
    )

    description = models.CharField(
        max_length = 520,
        blank = False
    )


    maxNumberOfParticipants = models.PositiveIntegerField(
        verbose_name = "Maximum Number Of Participants (2 - 96)",
        blank = False,
        default = 16,
        null = True,
        validators=[
            MinValueValidator(2),
            MaxValueValidator(96)
        ]
    )

    deadline = models.DateField(
        verbose_name = "Sign Up Deadline (YYYY-MM-DD)",
        blank = False,
        default=datetime.date.today,
        validators = [validate_date]
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE)


    location = models.CharField(max_length=255, blank = False,null= True)

    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank = False, null = False)

    organiser = models.ForeignKey(User, on_delete=models.CASCADE,blank = False, null= True,related_name="organiser")

    participants = models.ManyToManyField(User, blank = True)

    users_interested_in_event = models.ManyToManyField(User,blank =True, related_name ="interested_users")

    def get_people_that_responded_to_event(self):
        return self.participants.all().count() + self.users_interested_in_event.all().count()

    def get_number_of_users_going_to_event(self):
        return self.participants.all().count()

    def get_number_of_users_interested_in_event(self):
        return self.users_interested_in_event.all().count()

    def add_user_to_interested_field(self,club_member):
        if self.is_interested_in_event(club_member):
            self.remove_user_from_interested_field(club_member)
        else:
           self.users_interested_in_event.add(club_member)

    def remove_user_from_interested_field(self,club_member):
        self.users_interested_in_event.remove(club_member)

    def is_interested_in_event(self,club_member):
        return club_member in self.users_interested_in_event.all()

    def join_event(self, club_member):
        if self.is_part_of_event(club_member) :
            self.remove_from_event(club_member)

        elif self.is_interested_in_event(club_member) and self.participants.count() < self.maxNumberOfParticipants:
            self.remove_user_from_interested_field(club_member)
            self.add_memeber_to_event(club_member)

        elif self.participants.count() < self.maxNumberOfParticipants:
            self.add_memeber_to_event(club_member)

    def is_part_of_event(self, user):
        return user in self.participants.all()

    def remove_from_event(self, user):
        self.participants.remove(user)

    def add_memeber_to_event(self,user):
        self.participants.add(user)

    def check_past_event(self):
        return date.today()

# Create the Chat model
class Message(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, null=True, related_name='receiver', on_delete=models.CASCADE)
    club = models.ForeignKey(Club, null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=20, blank=False)

    def get_username(self):
        return self.user.username

# Create the Event's Posts model
class EventPost(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Model options."""

        ordering = ['-created_at']

# Create the Membership's Posts model
class MembershipPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    join = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def description(self):
        if self.join == True:
            return 'has joined this club'
        else:
            return 'has left this club'

    class Meta:
        """Model options."""

        ordering = ['-created_at']


# Create User made Posts model
class UserPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes= models.ManyToManyField(User, related_name="post_likes", blank=True)


    def number_of_likes(self):
        return self.likes.count()

    def has_liked(self,user):
        if self.likes.filter(id=user.id).exists():
            return True
        else:
            return False

    class Meta:
        """Model options."""

        ordering = ['-created_at']

# Create the Comment model
class Comment(models.Model):
    post = models.ForeignKey(UserPost,
                             on_delete=models.CASCADE,
                             related_name='comments')
    body = models.CharField(max_length=100)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user.username, self.post)
