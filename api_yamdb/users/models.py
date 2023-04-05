from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель Пользователя."""

    class ChoicesRole(models.TextChoices):
        USER_ROLE = ("user", "Пользователь")
        ADMIN_ROLE = ("admin", "Администратор")
        MODERATOR_ROLE = ("moderator", "Модератор")

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name="Email:",
        help_text="Укажите действующий Email.",
    )
    bio = models.TextField(
        null=True,
        verbose_name="О себе:",
        help_text="Напишите несколько строк о себе.",
    )
    role = models.CharField(
        max_length=16,
        choices=ChoicesRole.choices,
        default=ChoicesRole.USER_ROLE,
        verbose_name="Роль:",
        help_text="Выберите роль: пользователь, модератор или администратор.",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователь"

    def __str__(self):
        return f"username: {self.username}, email: {self.email}"
