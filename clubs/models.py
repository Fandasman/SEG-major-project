import datetime
from django.db import models
from .helpers import get_genres
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

    def gravatar(self, size = 120):
        g_object = Gravatar(self.email)
        url = g_object.get_image(size = size, default = 'mp')

    def mini_gravatar(self):
        return self.gravatar(size = 60)

# Create the Book model
class Book(models.Model):
    isbn = models.CharField(max_length = 17, unique = True, blank = False)
    title = models.CharField(max_length = 100, unique = True, blank = False)
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

    description = models.CharField(max_length = 500, blank = True)