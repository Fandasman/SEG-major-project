import datetime
from secrets import choice
from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from libgravatar import Gravatar
from multiselectfield import MultiSelectField


GENRE_CHOICES = [
    ('Fiction','Fiction'),
    ('Food and Drink','Food and Drink'),
    ('Science Fiction','Science Fiction'),
    ('Classics','Classics'),
    ('Nonfiction','Nonfiction'),
    ('Horror','Horror'),
    ('Mystery','Mystery'),
    ('Philosophy','Philosophy'),
    ('Business','Business'),
    ('Historical','Historical'),
    ('Romance','Romance'),
    ('Crime','Crime'),
    ('Womens Fiction','Womens Fiction'),
    ('Fantasy','Fantasy'),
    ('Young Adult','Young Adult'),
    ('Sequential Art','Sequential Art'),
    ('Politics','Politics'),
    ('Childrens','Childrens'),
    ('History','History'),
    ('Self Help','Self Help'),
    ('Humor','Humor'),
    ('Thriller','Thriller'),
    ('Autobiography','Autobiography'),
    ('Poetry','Poetry'),
    ('Short Stories','Short Stories'),
    ('Language','Language'),
    ('Science','Science'),
    ('Travel','Travel'),
    ('Parenting','Parenting'),
    ('Paranormal','Paranormal'),
    ('Biography','Biography'),
    ('Christian','Christian'),
    ('European Literature','European Literature'),
    ('Psychology','Psychology'),
    ('Adventure','Adventure'),
    ('Religion','Religion'),
    ('Holiday','Holiday'),
    ('Animals','Animals'),
    ('Christian Fiction','Christian Fiction'),
    ('Reference','Reference'),
    ('Spirituality','Spirituality'),
    ('Feminism','Feminism'),
    ('Health','Health'),
    ('Cultural','Cultural'),
    ('Adult Fiction','Adult Fiction'),
    ('Writing','Writing'),
    ('Realistic Fiction','Realistic Fiction'),
    ('Law','Law'),
    ('Art','Art'),
    ('Plays','Plays'),
    ('Relationships','Relationships'),
    ('Westerns','Westerns'),
    ('Sports','Sports')
]

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
    genres_preferences = MultiSelectField(choices=GENRE_CHOICES, max_choices=5, blank=True)

    

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

# Create the Books and Ratings model
class BooksRatings(models.Model):
    isbn = models.CharField(max_length = 13, blank = False)
    rating = models.IntegerField(
        validators = [MaxValueValidator(5), MinValueValidator(1)]
    )
    user = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)


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