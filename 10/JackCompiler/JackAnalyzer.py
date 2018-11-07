import argparse

from CompilationEngine import CompilationEngine
from FileHelper import *
from JackTokenizer import JackTokenizer


input_file_extension = '.jack'
output_file_extension = '.xml'

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path')
    args = parser.parse_args()
    return args.input_path


def get_output_file_path(input_file_path):
    return os.path.splitext(input_file_path)[0] + output_file_extension


def analyze_file(file):
    if get_file_extension(file) == input_file_extension:
        with open(get_output_file_path(file), "wb") as output_file:
            CompilationEngine(JackTokenizer(file), output_file)


def main():
    input_path = parse_arguments()
    if os.path.isfile(input_path):
        analyze_file(input_path)
    elif os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            file = os.path.join(input_path, filename)
            if os.path.isfile(file):
                analyze_file(file)
    else:
        print("You need to provide valid path to a jack file or a directory.")


if __name__ == '__main__':
    main()