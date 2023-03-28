from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import FileUploadForm
from ALC_dialog.ALC.ALC import ALC
from django.core.files.storage import FileSystemStorage
from os import path, getcwd
import os
from django.conf import settings

from typing import List, Dict, Union
from .models import UploadedFile


def run_check(files_data: List[Dict[str: str]]) -> None:
    print(files_data)
    pass


def execute(request: WSGIRequest) -> None:
    if request.method == 'POST':
        files_data = list()
        for file_name in request.FILES.keys():
            data = dict()
            file = request.FILES[file_name]
            file_type = file_name.split('.')[-1]
            uploaded_file = UploadedFile(file=file, name=file_name, type=file_type)
            uploaded_file.save()

            file_path = uploaded_file.file.path
            data['file_name'] = file_name
            data['file_path'] = file_path
            files_data.append(data)
        run_check(files_data)
        return redirect('ALC_dialog')
    else:
        form = FileUploadForm()
    return render(request, 'main.html', {'form': form})
