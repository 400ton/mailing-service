from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, max_length=35, verbose_name='Почта')
    avatar = models.ImageField(upload_to='users/avatars', verbose_name='Аватар', **NULLABLE)
    num_phone = models.CharField(unique=True, max_length=35, verbose_name='Телефон', **NULLABLE)
    country = models.CharField(verbose_name='Страна', **NULLABLE)

    verification_code = models.CharField(max_length=100, verbose_name='Код подтверждения', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} "

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
