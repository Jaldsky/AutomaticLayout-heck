import zipfile
import os

def unzip_archive(file_path, destination_path):
    if not os.path.exists(file_path):
        print(f"Error: Archive file '{file_path}' does not exist.")
        return
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(destination_path)

file_path = r'C:\Users\Jald\PycharmProjects\AutomaticLayoutCheck\AutomaticLayoutCheck\ALC_dialog\ALC\uploads\site_example.zip'
destination_path = r'C:\Users\Jald\PycharmProjects\AutomaticLayoutCheck\AutomaticLayoutCheck\ALC_dialog\ALC\data\test'

x = unzip_archive(file_path, destination_path)
print(x)
