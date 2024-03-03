from os import path, getcwd
import zipfile
from typing import Optional


def format_path(path: str) -> str:
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


def get_scan_paths(path: str, exclude_types: Optional[tuple]) -> Optional[list]:
    if exclude_types:
        for exclude_type in exclude_types:
            if 'exclude_type' == 'file':
                pass
            elif 'exclude_type' == 'folder':
                pass


class UnZipFileException(Exception):

    def __str__(self):
        return 'Unsupported archive type'
