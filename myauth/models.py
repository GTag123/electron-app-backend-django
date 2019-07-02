from __future__ import unicode_literals
from django.db import models
from django.db.transaction import atomic
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser): # , PermissionsMixin
    age = models.IntegerField(blank=True, null=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self
