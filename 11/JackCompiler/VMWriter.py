import ArithmeticCommandType as ArithmeticCommandType
import MemorySegmentType as MemorySegmentType


class VMWriter:

    def __init__(self, output_file):
        self._output_file = open(output_file, "w")

    def write_push(self, segment, i):
        self._write_to_file(self. _get_push(segment, i))

    def write_pop(self, segment, i):
        self._write_to_file(self. _get_pop(segment, i))

    def write_arithmetic(self, operation):
        self._write_to_file(self. _get_arithmetic(operation))

    def write_label(self, label):
        self._write_to_file(self. _get_label(label))

    def write_goto(self, label):
        self._write_to_file(self. _get_goto(label))

    def write_if_goto(self, label):
        self._write_to_file(self. _get_if_goto(label))

    def write_call(self, f_name, n_args):
        self._write_to_file(self. _get_call(f_name, n_args))

    def write_function(self, f_name, n_vars):
        self._write_to_file(self. _get_function(f_name, n_vars))

    def write_return(self):
        self._write_to_file(self. _get_return())

    def close_output_file(self):
        self._output_file.close()

    def _write_to_file(self, content):
        self._output_file.write(content + '\n')

    def _get_push(self, segment, i):
        return 'push ' + MemorySegmentType.get_string_from_type(segment) + ' ' + str(i)

    def _get_pop(self, segment, i):
        return 'pop ' + MemorySegmentType.get_string_from_type(segment) + ' ' + str(i)

    def _get_arithmetic(self, operation):
        return ArithmeticCommandType.get_string_from_type(operation)

    def _get_label(self, label):
        return 'label ' + label

    def _get_goto(self, label):
        return 'goto ' + label

    def _get_if_goto(self, label):
        return 'if-goto ' + label

    def _get_function(self, name, n_vars):
        return 'function ' + name + ' ' + str(n_vars)

    def _get_return(self):
        return 'return'

    def _get_call(self, f_name, n_args):
        return 'call ' + f_name + ' ' + str(n_args)
