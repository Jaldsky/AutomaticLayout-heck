from datetime import datetime
from django import setup
from os import environ, path, getcwd, walk, makedirs, remove
from shutil import rmtree
from zipfile import ZipFile, BadZipFile
from uuid import uuid4

from app.constants import ARCHIVE_EXPANSION
from app.utils.exceptions import (
    InvalidArchivePathException,
    ArchivePathNotFoundException,
    UnsupportedArchiveFormatException,
    UnZipFileException
)


def setup_environment() -> None:
    environ["DJANGO_SETTINGS_MODULE"] = "main.settings"
    setup()


def get_date_by_timestamp(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp/1000)


def unzip(archive_path: str, save_path: str | None = None) -> str | None:
    if not archive_path:
        raise InvalidArchivePathException

    if not path.exists(archive_path):
        raise ArchivePathNotFoundException

    if not save_path:
        save_path = path.splitext(archive_path)[0]

    _, extension = path.splitext(archive_path)
    if extension.lstrip('.') not in ARCHIVE_EXPANSION:
        raise UnsupportedArchiveFormatException
    try:
        with ZipFile(archive_path, 'r') as zip_ref:
            extract_path = path.join(getcwd(), save_path)
            zip_ref.extractall(extract_path)
            return extract_path
    except BadZipFile:
        raise UnZipFileException


def find_files_with_name(folder_path: str, key_file: str, inclusion: bool = False) -> list | None:
    paths = [
        path.join(dir_path, file_name)
        for dir_path, _, file_names in walk(folder_path)
        for file_name in file_names
        if file_name.lower() == key_file or
        inclusion and (key_file in file_name.lower())
    ]
    if not paths:
        return
    return paths


def get_uuid():
    return str(uuid4())


def extract_extension(filename: str) -> str:
    return filename.split('.')[-1]


def create_folder(folder_path: str) -> None:
    if not path.exists(folder_path):
        makedirs(folder_path)

# есть дубль в general TODO перенести в general
def remove_folder_or_file(folder_or_file_path: str) -> None:
    if path.exists(folder_or_file_path):
        if path.isfile(folder_or_file_path):
            remove(folder_or_file_path)
            return
        rmtree(folder_or_file_path)


def join_path(path_elements: list) -> str:
    return path.join(*path_elements)
