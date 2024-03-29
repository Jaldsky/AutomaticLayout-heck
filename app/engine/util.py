import uuid
import os
import shutil
import zipfile
from typing import Optional

SUPPORTED_ARCHIVE_FORMATS = ('zip', )


def unzip(archive_path: str, save_path: Optional[str] = None) -> Optional[str]:
    """Archive unpacking function.

    Args:
        archive_path: path to the archive.
        save_path: save path.
    #TODO Add doc
    """
    if not archive_path:
        raise InvalidArchivePathException

    if not os.path.exists(archive_path):
        raise ArchivePathNotFoundException

    if not save_path:
        save_path = os.path.splitext(archive_path)[0]

    _, extension = os.path.splitext(archive_path)
    if extension.lstrip('.') not in SUPPORTED_ARCHIVE_FORMATS:
        raise UnsupportedArchiveFormatException()

    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        try:
            extract_path = os.path.join(os.getcwd(), save_path)
            zip_ref.extractall(extract_path)
            return extract_path
        except Exception as e:
            raise UnZipFileException from e


def find_files_with_name(folder_path: str, key_file: str, inclusion: bool = False) -> Optional[list]:
    # TODO Add doc
    paths = [
        os.path.join(dir_path, file_name)
        for dir_path, _, file_names in os.walk(folder_path)
        for file_name in file_names
        if file_name.lower() == key_file or
        inclusion and (key_file in file_name.lower())
    ]
    if not paths:
        return
    return paths


def generate_uui():
    # TODO Add doc
    return str(uuid.uuid4())


def create_folder(folder_path: str) -> None:
    # TODO Add doc + test
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def remove_folder_or_file(folder_or_file_path: str) -> None:
    # TODO Add doc + test
    if os.path.exists(folder_or_file_path):
        if os.path.isfile(folder_or_file_path):
            os.remove(folder_or_file_path)
            return
        shutil.rmtree(folder_or_file_path)


def join_path(path_elements: list) -> str:
    return os.path.join(*path_elements)


class InvalidArchivePathException(Exception):

    def __str__(self):
        return "Invalid archive path provided."


class ArchivePathNotFoundException(Exception):
    def __str__(self):
        return "Archive path does not exist."


class UnsupportedArchiveFormatException(Exception):
    def __str__(self):
        return "Unsupported archive format."


class UnZipFileException(Exception):
    def __str__(self):
        return "Failed to unzip the archive."
