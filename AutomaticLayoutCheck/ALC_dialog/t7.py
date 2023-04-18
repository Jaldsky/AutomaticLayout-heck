from pyunpack import Archive
import os

def unzip_archive(file_path, destination_path):
    if not os.path.exists(file_path):
        print(f"Error: Archive file '{file_path}' does not exist.")
        return
    try:
        Archive(file_path).extractall(destination_path)
    except Exception as e:
        print(f"Error extracting archive '{file_path}': {e}")

file_path = r'C:\Users\Jald\PycharmProjects\AutomaticLayoutCheck\AutomaticLayoutCheck\ALC_dialog\ALC\uploads\06_CWxJg2U.rar'
destination_path = r'C:\Users\Jald\PycharmProjects\AutomaticLayoutCheck\AutomaticLayoutCheck\ALC_dialog\ALC\data'

# file_path = r'C:\Users\Jald\PycharmProjects\AutomaticLayoutCheck\AutomaticLayoutCheck\ALC_dialog\ALC\uploads\06_CWxJg2U.rar'
# destination_path = r'C:\Users\Jald\PycharmProjects\AutomaticLayoutCheck\AutomaticLayoutCheck\ALC_dialog\ALC\data'

x = unzip_archive(file_path, destination_path)
print(x)

