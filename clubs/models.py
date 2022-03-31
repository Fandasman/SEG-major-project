import datetime
from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from libgravatar import Gravatar
from datetime import date
from datetime import timedelta
from .validators import validate_date



# Create the Book model
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

# Create the Books and Ratings model
class BooksRatings(models.Model):
    isbn = models.CharField(max_length = 13, blank = False)
    rating = models.IntegerField(
        validators = [MaxValueValidator(5), MinValueValidator(1)]
    )
    user = models.ForeignKey(User, related_name='books', on_delete=models.CASCADE)


# Create the book Club model
class Club(models.Model):
    name = models.CharField(
        max_length = 50,
        unique = True,
        validators=[
            RegexValidator(
                regex = r'^.{3,}$',
                message = 'The name of the club must contain at least three characters!'
                )
        ]
    )
    location = models.CharField(max_length = 100, blank = False)
    description = models.CharField(max_length = 500, blank = False)
    club_book = models.ForeignKey(Book, related_name="club_book", blank = True, null = True, on_delete=models.CASCADE)

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

# Create the user's Roles model
ROLES= (
    ('A', 'Applicant'),
    ('M', 'Member'),
    ('O', 'Officer'),
    ('CO', 'Owner')
)

class Role(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    club= models.ForeignKey(Club, on_delete=models.CASCADE)
    role= models.CharField(
        max_length=2,
        choices=ROLES,
        default='A'
    )

    def get_club_name(self):
        return self.club.name


    def __str__(self):
        return self.user.full_name + " is " + self.role


# Create the Invitation model
STATUS={
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

    def get_club_name(self):
        return self.club.name

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
