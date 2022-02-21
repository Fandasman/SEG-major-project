import datetime
from django.db import models
from django.db.models import Q
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from libgravatar import Gravatar

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


class UserManager(models.Manager):
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
    imgURLSmall = models.URLField(blank = True)
    imgURLMedium = models.URLField(blank = True)
    imgURLLarge = models.URLField(blank = True)
    objects= BookManager()

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
    objects= UserManager(), UserAccountManager()

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
    objects = ClubManager()

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

    def get_club_name(self):
        return self.club.name

    def __str__(self):
        return self.user.full_name + " is " + self.role
