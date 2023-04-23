from typing import Dict
from os import path, getcwd, listdir, makedirs
from shutil import rmtree, move

from datetime import datetime
from json import loads
import logging

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from .models import UploadedFile, ProjectSettings
from .forms import FileUploadForm

from ALC_dialog.ALC.сontroller import Controller


logger = logging.getLogger(__name__)


def _create_results_folder() -> str:
    """Функция для создания папки для хранения кеша.

    Returns:
        Путь до созданной папки.
    """
    folder_name = f'result {datetime.now().strftime("%d.%m %H-%M-%S")}'
    folder_path = path.join(getcwd(), 'results', folder_name)
    if not path.exists(folder_path):
        makedirs(folder_path)
    return folder_path


def _move_uploaded_files(from_path: str, to_path: str) -> str:
    """Функция для перемещения файлов.

    Args:
        from_path: путь до файла, который необходимо перенести.
        to_path: путь для перемещения.

    Returns:
        Новый путь до файла.
    """
    return move(from_path, to_path)


def _delete_dir(dir_path: str) -> None:
    """Функция для удаления директории со всеми файлами и вложениями.

    Args:
        dir_path: путь до директории.
    """
    for file in listdir(dir_path):
        file_path = path.join(dir_path, file)
        try:
            rmtree(file_path)
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")


def _update_settings(params: Dict) -> Dict:
    """Функция для обновления настроек в проекте.

    Args:
        params: парамметры для сохранения.

    Returns:
        Словарь с сохраненными парамметрами.
    """
    project_settings = ProjectSettings.objects.first()

    project_settings.bedaub_text = bool(True if params.get('bedaub_text') else False)
    project_settings.clear_local_cache = bool(True if params.get('clear_local_cache') else False)
    project_settings.mse_comparator = bool(True if params.get('mse_comparator') else False)
    project_settings.ssim_comparator = bool(True if params.get('ssim_comparator') else False)
    project_settings.vgg16_comparator = bool(True if params.get('vgg16_comparator') else False)

    project_settings.save()
    return loads(str(project_settings))


def execute(request: WSGIRequest) -> None:
    """Функция для выполнения основной логики.

    Args:
        request: запрос от сервера.
    """
    if request.method == 'POST':
        settings = _update_settings(request.POST)

        folder_path = _create_results_folder()
        files_data = list()
        for request_type in request.FILES.keys():
            data = dict()
            file = request.FILES[request_type]
            file_extension = str(file).split('.')[-1]
            file_name = str(file).replace(file_extension, '').strip('.')
            uploaded_file = UploadedFile(name=file_name, type=file_extension)
            uploaded_file.upload_to = folder_path
            uploaded_file.save_file(file)

            data['file_extension'] = file_extension
            data['file_path'] = _move_uploaded_files(uploaded_file.file.path, folder_path)
            files_data.append(data)
        data = Controller().exec(files_data, folder_path)
        data['settings'] = settings
        if ProjectSettings.objects.get().clear_local_cache:
            _delete_dir(path.join(getcwd(), 'results'))
        return render(request, 'index.html', data)
    else:
        form = FileUploadForm()
    return render(request, 'index.html', {'form': form})
