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
    if not save_path:
        save_path = archive_path
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        zip_ref.extractall(save_path)


def get_scan_paths(path: str, exclude_types: Optional[tuple]) -> Optional[list]:
    if exclude_types:
        for exclude_type in exclude_types:
            if 'exclude_type' == 'file':
                pass
            elif 'exclude_type' == 'folder':
                pass
