from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('email address', unique=True, help_text='Required, Add a valid email address')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
