"""REST API для проверки и привязки Telegram ID."""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import UserAccount, TelegramBinding
from .serializers import UserAccountSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def telegram_check(request):
    """
    Проверяет, привязан ли telegram_id к какой-либо учётной записи.

    Если привязан – возвращает данные пользователя.
    Если нет – просто сообщает, что привязки нет.
    """
    telegram_id = request.data.get("telegram_id")

    if not telegram_id:
        return Response(
            {"detail": "Поле telegram_id обязательно"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        binding = TelegramBinding.objects.select_related("user").get(telegram_id=telegram_id)
    except TelegramBinding.DoesNotExist:
        return Response({"bound": False}, status=status.HTTP_200_OK)

    user_data = UserAccountSerializer(binding.user).data
    return Response({"bound": True, "user": user_data}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def bind_telegram(request):
    """
    Привязывает telegram_id к учётной записи.

    Ожидает:
    - telegram_id
    - username
    - password
    """
    telegram_id = request.data.get("telegram_id")
    username = request.data.get("username")
    password = request.data.get("password")

    if not telegram_id or not username or not password:
        return Response(
            {"detail": "Поля telegram_id, username и password обязательны"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = UserAccount.objects.get(username=username, is_active=True)
    except UserAccount.DoesNotExist:
        return Response(
            {"detail": "Неверный логин или пароль"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not user.check_password(password):
        return Response(
            {"detail": "Неверный логин или пароль"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # если привязка уже существует, не создаём дубль
    binding, _created = TelegramBinding.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={"user": user},
    )

    user_data = UserAccountSerializer(binding.user).data
    return Response({"bound": True, "user": user_data}, status=status.HTTP_200_OK)



