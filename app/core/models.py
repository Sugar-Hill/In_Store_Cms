from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class EmployeeManager(BaseUserManager):
    """
    Custom user model for employees where the email is the unique
    identifier for auth instead of usernames
    """
    # TODO: Add required fields such as firstname
    def create_employee(self, email, password, **extra_fields):
        """
        Create and save an employee with provided email and password.
        """
        if not email:
            raise ValueError(_('You must provide an email!'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save an admin employee with provided email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_employee(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    "Custom user model that supports using email instead of username"
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
