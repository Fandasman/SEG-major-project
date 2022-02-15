import datetime
from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from libgravatar import Gravatar

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

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size = 120):
        g_object = Gravatar(self.email)
        url = g_object.get_image(size = size, default = 'mp')

    def mini_gravatar(self):
        return self.gravatar(size = 60)

    def get_wishlist(self):
        return "\n".join([b.wishlist for b in self.wishlist.all()])


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
    leader = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'leader')
    members = models.ManyToManyField(User, related_name = 'member', blank = True)
    location = models.CharField(max_length = 100, blank = True)
    description = models.CharField(max_length = 500, blank = True)

    def get_members(self):
        return "\n".join([m.members for m in self.members.all()])

# Create the user's Roles model
ROLES= (
    ('A', 'Applicant'),
    ('M', 'Member'),
    ('O', 'Owner'),
)

class Role(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    club= models.ForeignKey(Club, on_delete=models.CASCADE)
    role= models.CharField(
        max_length=1,
        choices=ROLES,
        default='A'
    )

    def __str__(self):
        return self.user.full_name + " is " + self.role
