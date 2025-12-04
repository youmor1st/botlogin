"""Конфигурация приложения app."""
from django.apps import AppConfig


class AppConfig(AppConfig):
    """Конфиг приложения для регистрации в Django."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "app"



