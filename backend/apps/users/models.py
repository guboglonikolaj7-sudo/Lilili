from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator

class User(AbstractUser):
    username = None
    email = models.EmailField(
        "Email", 
        unique=True, 
        validators=[EmailValidator],
        error_messages={
            'unique': "Пользователь с таким email уже существует.",
        }
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
