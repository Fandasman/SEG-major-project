from django.db import models
from django.core.validators import RegexValidator
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