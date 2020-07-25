import uuid
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


def recipe_image_file_path(instance, filename):
    """"Generate file path for new product image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/product/', filename)


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
    # Store_id foreign key
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = EmployeeManager()

    USERNAME_FIELD = 'email'


class Product(models.Model):
    """Product model"""
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)
    price = models.FloatField()
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    products = models.ManyToManyField(Product)
    date_ordered = models.DateTimeField(auto_now_add=True)
    # Replace with choices field, drop-down
    is_fulfilled = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
