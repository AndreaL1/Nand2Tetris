import os

from ArithmeticCommandType import ArithmeticCommandType
from CommandType import CommandType
from Exceptions import *
from FileHelper import *
from MemorySegmentType import MemorySegmentType

_comment_sign = '//'


class Parser:

    def __init__(self, input_file_list):
        self._commands = self._get_commands(input_file_list)
        self._filenames = self._get_filenames(input_file_list)
        self._current_command_idx = -1
        self._current_file_idx = 0

    def has_more_commands(self):
        if self._current_file_idx < len(self._commands) - 1:
            return True
        else:
            return self._current_command_idx < len(self._commands[self._current_file_idx]) - 1

    def advance(self):
        if not self.has_more_commands():
            raise CommandOutOfBoundsError()
        if self._current_command_idx < len(self._commands[self._current_file_idx]) - 1:
            self._current_command_idx += 1
        else:
            self._current_file_idx +=1
            self._current_command_idx = 0

    def get_current_command(self):
        return self._commands[self._current_file_idx][self._current_command_idx]

    def command_type(self):
        cmd_type = CommandType.get_type_from_string(self._get_arg0())
        if cmd_type is not None:
            return cmd_type
        raise CommandError()

    def arg1(self):
        cmd_type = self.command_type()
        if cmd_type == CommandType.C_RETURN:
            return None
        if cmd_type == CommandType.C_PUSH or cmd_type == CommandType.C_POP:
            seg_type = MemorySegmentType.get_type_from_string(self._get_arg1())
            if seg_type is not None:
                return seg_type
            raise CommandError()
        if cmd_type == CommandType.C_ARITHMETIC:
            arith_cmd_type = ArithmeticCommandType.get_type_from_string(self._get_arithmetic_arg1())
            if arith_cmd_type is not None:
                return arith_cmd_type
            raise CommandError()
        else:
            arg1 = self._get_arg1()
            if arg1 is not None:
                return arg1
            raise CommandError()

    def arg2(self):
        cmd_type = self.command_type()
        if cmd_type == CommandType.C_ARITHMETIC or \
                        cmd_type == CommandType.C_LABEL or \
                        cmd_type == CommandType.C_GOTO or \
                        cmd_type == CommandType.C_IF_GOTO or \
                        cmd_type == CommandType.C_RETURN:
            return None
        arg = str.split(self.get_current_command(), " ")
        if len(arg) < 3:
            raise CommandError
        return arg[2]

    def get_current_filename(self):
        return self._filenames[self._current_file_idx]

    def _get_commands(self, file_list):
        files_content = []
        for file in file_list:
            files_content.append(read_file(file))
        return [_get_raw_instructions(content) for content in files_content]

    def _get_filenames(self, file_list):
        return [get_filename(file) for file in file_list]

    def _get_arg0(self):
        return str.split(self.get_current_command(), " ")[0]

    def _get_arg1(self):
        split_cmd = str.split(self.get_current_command(), " ")
        if len(split_cmd) < 2:
            raise CommandError
        return split_cmd[1]

    def _get_arithmetic_arg1(self):
        return str.split(self.get_current_command(), " ")[0]


def _get_raw_instructions(content):
    return _remove_empty_lines(_remove_comments(_strip_content(content)))


def _remove_comments(content):
    return [line[:line.find(_comment_sign)] if _comment_sign in line else line for line in content]


def _strip_content(content):
    return [x.strip() for x in content]


def _remove_empty_lines(content):
    return [line for line in content if len(line) > 0]
