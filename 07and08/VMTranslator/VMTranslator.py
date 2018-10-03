import argparse
import os
import sys
import traceback

from CodeWriter import CodeWriter
from CommandType import CommandType
from Exceptions import *
from FileHelper import *
from Parser import Parser


class VMTranslator:

    def __init__(self, input_file_list, output_file_path, write_bootstrap):
        self._parser = Parser(input_file_list)
        self._code_writer = CodeWriter(output_file_path)
        self._write_bootstrap = write_bootstrap

    def translate(self):
        if self._write_bootstrap:
            self._code_writer.write_bootstrap()
        while self._parser.has_more_commands():
            self._parser.advance()
            self._code_writer.set_current_filename(self._parser.get_current_filename())
            try:
                cmd_type = self._parser.command_type()
            except CommandError:
                self._handle_command_error()
                continue
    
            if cmd_type == CommandType.C_PUSH:
                try:
                    self._code_writer.write_push(self._parser.arg1(), self._parser.arg2())
                except CommandError:
                    self._handle_command_error()
                    continue
            if cmd_type == CommandType.C_POP:
                try:
                    self._code_writer.write_pop(self._parser.arg1(), self._parser.arg2())
                except CommandError:
                    self._handle_command_error()
                    continue
            if cmd_type == CommandType.C_ARITHMETIC:
                try:
                    self._code_writer.write_arithmetic(self._parser.arg1())
                except CommandError:
                    self._handle_command_error()
                    continue
            if cmd_type == CommandType.C_LABEL:
                try:
                    self._code_writer.write_label(self._parser.arg1())
                except CommandError:
                    self._handle_command_error()
                    continue
            if cmd_type == CommandType.C_GOTO:
                try:
                    self._code_writer.write_goto(self._parser.arg1())
                except CommandError:
                    self._handle_command_error()
                    continue
            if cmd_type == CommandType.C_IF_GOTO:
                try:
                    self._code_writer.write_if_goto(self._parser.arg1())
                except CommandError:
                    self._handle_command_error()
                    continue
            if cmd_type == CommandType.C_FUNCTION:
                try:
                    self._code_writer.write_function(self._parser.arg1(), self._parser.arg2())
                except CommandError:
                    self._handle_command_error()
                    continue
            if cmd_type == CommandType.C_RETURN:
                try:
                    self._code_writer.write_return()
                except CommandError:
                    self._handle_command_error()
                    continue
            if cmd_type == CommandType.C_CALL:
                try:
                    self._code_writer.write_call(self._parser.arg1(), self._parser.arg2())
                except CommandError:
                    self._handle_command_error()
                    continue
        self._code_writer.close_output_file()

    def _handle_command_error(self):
        print("Command " + self._parser.get_current_command() + ' is invalid.')


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file_path')
    args = parser.parse_args()
    return args.input_file_path


def get_output_file_path(input_file_path):
    return os.path.splitext(input_file_path)[0] + '.asm'


def get_output_file_path_from_dir(input_dir_path):
    return os.path.join(input_dir_path, os.path.basename(input_dir_path) + '.asm')


def translate_vm_to_asm(input_file_list, output_file_path, write_bootstrap):
    try:
        vm_translator = VMTranslator(input_file_list, output_file_path, write_bootstrap)
    except IOError as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("*** print_tb:")
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print("*** print_exception:")
        # exc_type below is ignored on 3.5 and later
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stdout)
       # print(traceback.print_exception(e))
        return
    vm_translator.translate()


def main():
    input_path = parse_arguments()
    file_list = []
    write_bootstrap = False
    if os.path.isfile(input_path):
        file_list.append(input_path)
        translate_vm_to_asm(file_list, get_output_file_path(input_path), write_bootstrap)

    elif os.path.isdir(input_path):
        write_bootstrap = True
        for filename in os.listdir(input_path):
            if get_file_extension(filename) == ".vm":
                file_list.append(os.path.join(input_path, filename))
        translate_vm_to_asm(file_list, get_output_file_path_from_dir(input_path), write_bootstrap)

    else:
        print("You need to provide valid path to a file or a directory.")


if __name__ == '__main__':
    main()
