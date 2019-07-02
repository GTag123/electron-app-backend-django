from __future__ import unicode_literals
from django.db import models
from django.db.transaction import atomic
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager, User, UserManager
)


class UserManager2(BaseUserManager):

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        try:
            with atomic(): # transaction.atomic()
                user = self.model(username=username, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(username, password=password, **extra_fields)


class AppUser(User): # , PermissionsMixin
    class Meta:
        proxy = True
        ordering = ('id', )
    objects = UserManager()
    # email = models.EmailField(max_length=40, unique=True)
    # username = models.CharField(max_length=20, unique=True)
    # first_name = models.CharField(max_length=30, blank=True)
    # last_name = models.CharField(max_length=30, blank=True)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # date_joined = models.DateTimeField(default=timezone.now)

    # objects = UserManager()

    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self
