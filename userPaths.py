import os
import glob

from CPsControllerDB import CPsLoadFromJson
from CPsControllerJson import ma_file_path

def CPsFilesContent():
    folder_path = os.path.dirname(__file__)
    files = glob.glob(os.path.join(folder_path, '*'))
    for file_path in files:
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                print(f'Content of {file_path}:\n{content}\n')

def CPsImagePath(image_name):
    
    current_dir = os.path.dirname(__file__)
    images_dir = os.path.join(current_dir, '..', 'images')
    image_path = os.path.join(images_dir, image_name)
    return image_path


def ImagePath(image_name):
    base_path = "D:/clumsypanda/Documents/maya/scripts/clumsyPandaTools/images/"
    return os.path.join(base_path, image_name)



def controller():

    return ma_file_path


