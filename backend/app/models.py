"""Модели для хранения учётных записей и привязок Telegram."""
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class UserAccount(models.Model):
    """Простая учётная запись, которую создаёт админ."""

    # логин, который выдаёт админ
    username = models.CharField(max_length=150, unique=True)
    # хэш пароля
    password = models.CharField(max_length=255)
    # флаг активности
    is_active = models.BooleanField(default=True)

    def set_password(self, raw_password: str) -> None:
        """Сохраняет хэш пароля вместо открытого текста."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """Проверяет введённый пароль по хэшу."""
        return check_password(raw_password, self.password)

    def __str__(self) -> str:
        """Строковое представление учётной записи."""
        return self.username


class TelegramBinding(models.Model):
    """Связь telegram_id с конкретной учётной записью."""

    # строковый Telegram ID
    telegram_id = models.CharField(max_length=64, unique=True)
    # связанная учётка
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="bindings")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Строковое представление привязки."""
        return f"{self.telegram_id} -> {self.user.username}"



