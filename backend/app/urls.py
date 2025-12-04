"""Маршрутизация для приложения app."""
from django.urls import path
from . import views


urlpatterns = [
    path("auth/telegram-check/", views.telegram_check, name="telegram_check"),
    path("auth/bind/", views.bind_telegram, name="bind_telegram"),
]



