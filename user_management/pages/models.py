from django.db import models
from django.utils.timezone import now
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission

class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('An Email is required.')
        if not password:
            raise ValueError('A Password is required.')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError('An Email is required.')
        if not password:
            raise ValueError('A Password is required.')
        user = self.create_user(email, password)
        user.is_superuser = True
        user.save()
        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=now)
    password = models.CharField(max_length=300)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
