import os

def get_file_extension(file):
    return os.path.splitext(file.name)[1].replace('.', '')

