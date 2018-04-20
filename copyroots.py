import shutil
import os

folder_path = "D:/rod/all COD/cif/"
newpath = "D:/cif/"

for path, dirs, files in os.walk(folder_path):
    for filename in files:
        shutil.copy2(filename, newpath)

