from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom manager for the User model where email is the unique identifier
    for authentication instead of usernames.
    """
    
    def create_user(self, email, fullname, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, fullname, and password.
        """

        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, password=None, **extra_fields):
        """
        Creates and saves a SuperUser with admin privileges.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, fullname, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model for KanMind.
    - Removes 'username' field.
    - Uses 'email' as the primary login identifier.
    - Adds 'fullname' for better user profile representation.
    """

    username = None
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    def __str__(self):
        """Returns the email address as the string representation."""
        return self.email