from django.contrib.auth.models import User, PermissionsMixin


class Profile(User, PermissionsMixin):
    """
    We inherit django model User to be able to extend it and add some additional fields such as 'date of birth' or
    'profile image'.
    """
    # New fields go here

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Profile'