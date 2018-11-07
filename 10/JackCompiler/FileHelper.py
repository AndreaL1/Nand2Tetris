import os


def read_file(file):
    with open(file) as f:
        content = f.readlines()
    return content


def get_filename(full_path):
    return os.path.splitext(os.path.basename(full_path))[0]


def get_file_extension(full_path):
    return os.path.splitext(os.path.basename(full_path))[1]
