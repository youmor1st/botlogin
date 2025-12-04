"""Регистрация моделей в админке Django."""
from django.contrib import admin
from .models import UserAccount, TelegramBinding


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    """Отображение и управление учётными записями в админке."""

    list_display = ("id", "username", "is_active")
    search_fields = ("username",)

    def save_model(self, request, obj, form, change):
        """
        Переопределяем сохранение, чтобы хэшировать пароль,
        если его изменили через админку.
        """
        password_field = "password"
        if password_field in form.changed_data:
            raw_password = form.cleaned_data[password_field]
            obj.set_password(raw_password)
        super().save_model(request, obj, form, change)


@admin.register(TelegramBinding)
class TelegramBindingAdmin(admin.ModelAdmin):
    """Отображение привязок Telegram ID в админке."""

    list_display = ("id", "telegram_id", "user", "created_at")
    search_fields = ("telegram_id", "user__username")



