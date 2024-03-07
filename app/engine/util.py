from os import path, getcwd, walk
import zipfile
from typing import Optional


def format_path(path: str) -> str:
    # TODO find out if this method is needed
    pass


def unzip(archive_path: str, save_path: Optional[str] = None) -> None:
    """Archive unpacking function.

    Args:
        archive_path: path to the archive.
        save_path: save path.
    """
    folder_save_path, extension = path.splitext(archive_path)
    if extension.lstrip('.') not in ('zip', ):
        raise UnZipFileException

    if not save_path:
        save_path = folder_save_path
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        zip_ref.extractall(path.join(getcwd(), save_path))


def search_folder_key_file_paths(folder_path: str, key_file: str) -> Optional[list]:
    return [path.join(dir_path, file_name)
            for dir_path, _, file_names in walk(folder_path)
            for file_name in file_names
            if file_name.lower() == key_file]


class UnZipFileException(Exception):

    def __str__(self):
        return 'Unsupported archive type'
