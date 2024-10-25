from django.contrib.auth.models import AbstractUser

from django.db import models


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """
    Модель пользователя.
    """

    username = None
    email = models.EmailField(verbose_name='электронный адрес', unique=True)
    tg_chat_id = models.CharField(max_length=50, verbose_name="Телеграм chat id", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email