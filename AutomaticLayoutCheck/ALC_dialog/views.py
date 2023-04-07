from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import FileUploadForm
from ALC_dialog.ALC.Controller import Controller
from django.core.files.storage import FileSystemStorage
from os import path, getcwd, makedirs, rename
from django.conf import settings
from datetime import datetime
from typing import List, Dict, Union
from .models import UploadedFile
import logging
import shutil



logger = logging.getLogger(__name__)


def create_results_folder() -> str:
    "return path"
    folder_name = f'result {datetime.now().strftime("%d.%m %H-%M-%S")}'
    folder_path = path.join(getcwd(), 'results', folder_name)
    if not path.exists(folder_path):
        makedirs(folder_path)
    return folder_path


def _move_uploaded_files(from_path: str, to_path: str) -> str:
    'doc'
    return shutil.move(from_path, to_path)


def execute(request: WSGIRequest) -> None:
    'doc'
    if request.method == 'POST':
        folder_path = create_results_folder()
        files_data = list()
        for request_type in request.FILES.keys():
            data = dict()
            file = request.FILES[request_type]
            file_name, file_extension = str(file).split('.')

            uploaded_file = UploadedFile(name=file_name, type=file_extension)
            uploaded_file.upload_to = folder_path
            uploaded_file.save_file(file)

            data['file_extension'] = file_extension
            data['file_path'] = _move_uploaded_files(uploaded_file.file.path, folder_path)
            files_data.append(data)
        Controller(files_data, folder_path).exec()
        return redirect('ALC_dialog')
    else:
        form = FileUploadForm()
    return render(request, 'main.html', {'form': form})
