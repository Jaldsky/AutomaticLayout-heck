from django.core.files.uploadedfile import TemporaryUploadedFile
from django.shortcuts import render, redirect
from .forms import FileUploadForm
from ALC_dialog.ALC.ALC import ALC
from django.core.files.storage import FileSystemStorage
from os import path, getcwd


def execute(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)

        file1 = _save_file(request.FILES['file1'])
        file2 = _save_file(request.FILES['file2'])


        ALC(file1, file2).exec()
    else:
        form = FileUploadForm()
    return render(request, 'main.html', {'form': form})


def _save_file(file: TemporaryUploadedFile):
    # Create an instance of FileSystemStorage to handle file storage
    fs = FileSystemStorage()

    # Get the file path from the TemporaryUploadedFile object
    file_path = file.temporary_file_path()

    # Use the FileSystemStorage instance to save the file
    saved_file_path = fs.save("file", file)

    # You can also delete the TemporaryUploadedFile object
    # after saving the file
    file.close()
    print(saved_file_path)
    # Return the saved file path
    return saved_file_path



