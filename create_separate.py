import os
import shutil
import glob
from distutils.dir_util import copy_tree

base_folder = os.path.join(os.path.dirname(__file__), 'data')
report_folder = os.path.join(base_folder, 'Report')

excel_folder = os.path.join(base_folder, 'Excel')
os.makedirs(excel_folder, exist_ok=True)
files = glob.iglob(os.path.join(report_folder, "**/**/**/**/*.xlsx"), recursive=True)
for file in files:
    if os.path.isfile(file):
        file_path = os.path.dirname(os.path.dirname(
            os.path.join(base_folder, os.path.relpath(file, excel_folder).replace('../Report', 'Excel'))))
        if not file_path.endswith('100'):
            file_path = os.path.dirname(file_path)
        os.makedirs(file_path, exist_ok=True)
        shutil.copy2(file, file_path)

binary_folder = os.path.join(base_folder, 'Binary')
os.makedirs(binary_folder, exist_ok=True)
files = glob.iglob(os.path.join(report_folder, "**/**/BINARY/**/**/**/**/*.png"), recursive=True)
for file in files:
    if os.path.isfile(file):
        file_path = os.path.dirname(os.path.join(base_folder,
                                                 os.path.relpath(file, binary_folder).replace('/BINARY', '').replace(
                                                     '../Report',
                                                     'Binary')))
        os.makedirs(file_path, exist_ok=True)
        shutil.copy2(file, file_path)

grey_folder = os.path.join(base_folder, 'Gray')
os.makedirs(grey_folder, exist_ok=True)
files = glob.iglob(os.path.join(report_folder, "**/**/GRAY_CODE/**/**/**/**/*.png"), recursive=True)
for file in files:
    if os.path.isfile(file):
        file_path = os.path.dirname(os.path.join(base_folder,
                                                 os.path.relpath(file, grey_folder).replace('/GRAY_CODE', '').replace(
                                                     '../Report',
                                                     'Gray')))
        os.makedirs(file_path, exist_ok=True)
        shutil.copy2(file, file_path)

fhd_folder = os.path.join(base_folder, 'Binary_Func')
os.makedirs(fhd_folder, exist_ok=True)
files = glob.iglob(os.path.join(binary_folder, "**/FHD/**/**/**/**/*.png"), recursive=True)
for file in files:
    if os.path.isfile(file):
        file_path = os.path.dirname(os.path.join(base_folder,
                                                 os.path.relpath(file, fhd_folder).replace(
                                                     '../Binary',
                                                     'Binary_Func')))
        os.makedirs(file_path, exist_ok=True)
        shutil.copy2(file, file_path)

shutil.rmtree(os.path.join(binary_folder, "**/FHD/**"))
