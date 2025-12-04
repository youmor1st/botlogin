#!/usr/bin/env python
"""Утилита командной строки Django."""
import os
import sys


def main():
    """Точка входа в Django-проект."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Убедитесь, что Django установлен в окружении."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()



