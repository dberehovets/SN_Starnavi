from django.db import models
from django.contrib.auth.models import User, PermissionsMixin


class Profile(User, PermissionsMixin):

    def __str__(self):
        return f"@{self.username}"

    class Meta:
        verbose_name = 'Profile'
