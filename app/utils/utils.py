from datetime import datetime

from django import setup
from os import environ


def setup_environment() -> None:
    environ["DJANGO_SETTINGS_MODULE"] = "main.settings"
    setup()


def get_date_by_timestamp(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp/1000)
