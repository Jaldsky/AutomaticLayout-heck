import logging
from dataclasses import dataclass
from enum import Enum


@dataclass
class FormException(Exception):
    """Базовая форма для исключений."""

    message: str

    def __str__(self) -> str:
        """Строковое представление исключения."""
        return self.message

class StringEnum(str, Enum):
    """Базовая форма для энумерации."""

    def __str__(self) -> str:
        """Магический метод возвращения строкового представления.

        Returns:
            Строковое представление.
        """
        return str.__str__(self)


def setup_logging(level=logging.INFO, **kwargs) -> logging.Logger:
    """Функция логирования.

    Args:
        level: Уровень логирования для установки.
        **kwargs: Дополнительные именованные аргументы для настройки логирования.

    Returns:
        Объект логгера для регистрации сообщений.
    """
    logging.basicConfig(level=level, **kwargs)
    logger = logging.getLogger(__name__)
    return logger
