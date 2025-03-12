from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    We can add extra fields if needed.
    """
    pass
