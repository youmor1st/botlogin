"""Сериализаторы для REST API."""
from rest_framework import serializers
from .models import UserAccount


class UserAccountSerializer(serializers.ModelSerializer):
    """Сериализатор для отдачи базовых данных пользователя."""

    class Meta:
        model = UserAccount
        fields = ["id", "username"]



