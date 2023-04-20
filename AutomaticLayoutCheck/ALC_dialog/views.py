from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import FileUploadForm
from ALC_dialog.ALC.сontroller import Controller
from django.core.files.storage import FileSystemStorage
from os import path, getcwd, makedirs, rename
from django.conf import settings
from datetime import datetime
from typing import List, Dict, Union
from .models import UploadedFile
import logging
import shutil

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from AutomaticLayoutCheck.settings import ENABLE_CLEAR_LOCAL_CACHE
from shutil import rmtree
from os import path, getcwd, scandir, pardir, listdir


logger = logging.getLogger(__name__)


def _create_results_folder() -> str:
    "return path"
    folder_name = f'result {datetime.now().strftime("%d.%m %H-%M-%S")}'
    folder_path = path.join(getcwd(), 'results', folder_name)
    if not path.exists(folder_path):
        makedirs(folder_path)
    return folder_path


def _move_uploaded_files(from_path: str, to_path: str) -> str:
    'doc'
    return shutil.move(from_path, to_path)

def _delete_dir(dir_path: str):
    for file in listdir(dir_path):
        file_path = path.join(dir_path, file)
        try:
            rmtree(file_path)
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")

def execute(request: WSGIRequest) -> None:
    'doc'
    if request.method == 'POST':
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
        if ENABLE_CLEAR_LOCAL_CACHE:
            _delete_dir(path.join(getcwd(), 'results'))
        return render(request, 'index.html', data)
    else:
        form = FileUploadForm()
    return render(request, 'index.html', {'form': form})
