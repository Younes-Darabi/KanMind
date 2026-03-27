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
        
        """Standardize the email address (lowercase the domain part)"""
        email = self.normalize_email(email)

        """Create a new user instance"""
        user = self.model(email=email, fullname=fullname, **extra_fields)

        """Hash the password before saving"""
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, fullname, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model that uses email as the primary login field.
    The default 'username' field is removed.
    """
    """Remove the default username field"""
    username = None

    """Custom fields for our project requirements"""
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)

    """Assign the custom manager"""
    objects = UserManager()

    """Set email as the unique identifier for logging in"""
    USERNAME_FIELD = 'email'

    """Fields required when creating a user via 'createsuperuser' command"""
    REQUIRED_FIELDS = ['fullname']

    def __str__(self):
        """
        Returns the email address as the string representation of the user object.
        """
        return self.email