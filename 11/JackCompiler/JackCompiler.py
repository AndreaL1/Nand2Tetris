import argparse

from CompilationEngine import CompilationEngine
from FileHelper import *
from JackTokenizer import JackTokenizer
from VMWriter import VMWriter

input_file_extension = '.jack'
output_file_extension = '.vm'

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path')
    args = parser.parse_args()
    return args.input_path


def get_output_file_path(input_file_path):
    return os.path.splitext(input_file_path)[0] + output_file_extension


def compile_file(file):
    if get_file_extension(file) == input_file_extension:
        output_file = get_output_file_path(file)
        CompilationEngine(JackTokenizer(file), VMWriter(output_file))


def main():
    input_path = parse_arguments()
    if os.path.isfile(input_path):
        compile_file(input_path)
    elif os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            file = os.path.join(input_path, filename)
            if os.path.isfile(file):
                compile_file(file)
    else:
        print("You need to provide valid path to a jack file or a directory.")


if __name__ == '__main__':
    main()
