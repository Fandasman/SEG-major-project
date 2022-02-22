# from asyncio.windows_events import NULL
import datetime
from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from libgravatar import Gravatar

# Create your models here.

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

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
        
    def gravatar(self, size = 120):
        g_object = Gravatar(self.email)
        url = g_object.get_image(size = size, default = 'mp')

    def mini_gravatar(self):
        return self.gravatar(size = 60)

# Create the Book model
class Book(models.Model):
    isbn = models.CharField(max_length = 13, unique = True, blank = False, primary_key=True)
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
    current_book = models.ForeignKey(Book, on_delete = models.DO_NOTHING, default=None, blank=True)
    book_page = models.IntegerField(default = 0, blank=True, 
    validators = [MaxValueValidator(9999), MinValueValidator(0)])

    def get_members(self):
        return "\n".join([m.members for m in self.members.all()])
