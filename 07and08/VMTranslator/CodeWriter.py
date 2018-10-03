from ArithmeticCommandType import *
from CodeWriterHelper import *
from Exceptions import *
from FileHelper import *
from MemorySegmentType import *

#Functions starting with 'write_' throw Attribute Error if the output_file is
#not set in the constructor call.

class CodeWriter:
    _tmp_address = 'addr'
    _THAT = 'THAT'
    _THIS = 'THIS'
    _temp_segment_start_address = '5'
    _this_pointer_symbol = '0'
    _that_pointer_symbol = '1'
    _end_frame = 'endFrame'
    _SP_start_address = '256'
    _start_function = 'Sys.init'

    def __init__(self, output_file=None):
        if output_file is not None:
            self._output_file = open(output_file, "w")
            self._output_filename = get_filename(output_file)
        else:
            self._output_file = None
        self._current_filename = None
        self._cmp_op_cnt = 0
        self._f_ret_cnt = {}

    def set_current_filename(self, filename):
        self._current_filename = filename

    def write_bootstrap(self):
        self._write_to_file(set_sp_to_value(self._SP_start_address))
        self.write_call(self._start_function, '0')

    def write_push(self, segment, i):
        if self._output_file is not None:
            command = self.get_push(segment, i)
            self._write_to_file(command)
        else:
            raise NoOutputFileError()

    def write_pop(self, segment, i):
        if self._output_file is not None:
            command = self.get_pop(segment, i)
            self._write_to_file(command)
        else:
            raise NoOutputFileError()

    def write_arithmetic(self, operation):
        if self._output_file is not None:
            if is_add(operation):
                self._write_to_file(self.get_add())
            elif is_sub(operation):
                self._write_to_file(self.get_sub())
            elif is_neg(operation):
                self._write_to_file(self.get_neg())
            elif is_and(operation):
                self._write_to_file(self.get_and())
            elif is_or(operation):
                self._write_to_file(self.get_or())
            elif is_not(operation):
                self._write_to_file(self.get_not())
            elif is_eq(operation):
                self._write_to_file(self.get_eq())
            elif is_lt(operation):
                self._write_to_file(self.get_lt())
            elif is_gt(operation):
                self._write_to_file(self.get_gt())
            else:
                raise CommandError("Invalid command.")
        else:
            raise NoOutputFileError()

    def write_label(self, label):
        self._write_to_file(self.get_label(label))

    def write_goto(self, label):
        if self._output_file is not None:
            self._write_to_file(self.get_goto(label))
        else:
            raise NoOutputFileError()

    def write_if_goto(self, label):
        if self._output_file is not None:
            self._write_to_file(self.get_if_goto(label))
        else:
            raise NoOutputFileError()

    def write_function(self, f_name, n_vars):
        if self._output_file is not None:
            self._write_to_file(self.get_function(f_name, n_vars))
        else:
            raise NoOutputFileError()

    def write_return(self):
        if self._output_file is not None:
            self._write_to_file(self.get_return())
        else:
            raise NoOutputFileError()

    def write_call(self, f_name, n_args):
        if self._output_file is not None:
            self._write_to_file(self.get_call(f_name, n_args))
        else:
            raise NoOutputFileError()

    def get_push(self, segment, i):
        if is_basic_segment(segment):
            return self.get_push_basic_segment(segment, i)
        if is_const_segment(segment):
            return self.get_push_const_segment(i)
        if is_static_segment(segment):
            return self.get_push_static_segment(i)
        if is_temp_segment(segment):
            return self.get_push_temp_segment(i)
        if is_pointer_segment(segment):
            return self.get_push_pointer_segment(i)

    def get_pop(self, segment, i):
        if is_basic_segment(segment):
            return self.get_pop_basic_segment(segment, i)
        if is_static_segment(segment):
            return self.get_pop_static_segment(i)
        if is_temp_segment(segment):
            return self.get_pop_temp_segment(i)
        if is_pointer_segment(segment):
            return self.get_pop_pointer_segment(i)

    def get_add(self):
        return pop_to_d() + pop_add_to_d() + push_from_d()

    def get_sub(self):
        return pop_to_d() + pop_sub_to_d() + push_from_d()

    def get_neg(self):
        return pop_neg_to_d() + push_from_d()

    def get_and(self):
        return pop_to_d() + pop_and_to_d() + push_from_d()

    def get_or(self):
        return pop_to_d() + pop_or_to_d() + push_from_d()

    def get_not(self):
        return pop_not_to_d() + push_from_d()

    def get_eq(self):
        self._cmp_op_cnt += 1
        return pop_to_d() + pop_sub_to_d() + write_to_d_eq_d_to_zero(self._cmp_op_cnt - 1) + push_from_d()

    def get_lt(self):
        self._cmp_op_cnt += 1
        return pop_to_d() + pop_sub_to_d() + write_to_d_lt_d_to_zero(self._cmp_op_cnt - 1) + push_from_d()

    def get_gt(self):
        self._cmp_op_cnt += 1
        return pop_to_d() + pop_sub_to_d() + write_to_d_gt_d_to_zero(self._cmp_op_cnt - 1) + push_from_d()

    def get_label(self, label):
        return write_label(label)

    def get_goto(self, label):
        return set_address(label) + unconditional_jmp()

    def get_if_goto(self, label):
        return pop_to_d() + set_address(label) + jmp_not_equal()

    def get_function(self, name, n_vars):
        return self.get_label(name) + (self.get_push_const_segment('0')) * int(n_vars)

    def get_return(self):
        ret_addr_offset_from_end_frame = '5'
        that_offset_from_end_frame = '1'
        this_offset_from_end_frame = '2'
        arg_offset_from_end_frame = '3'
        lcl_offset_from_end_frame = '4'
        ret_addr = 'retAddr'
        return write_from_address_to_address(get_segment_pointer(MemorySegmentType.LOCAL), self._end_frame) \
               + write_to_address_from_address_minus_value(ret_addr, ret_addr_offset_from_end_frame) \
               + pop_to_pointer(get_segment_pointer(MemorySegmentType.ARGUMENT)) \
               + set_sp_to_arg_plus_one() \
               + write_to_address_from_address_minus_value(get_segment_pointer(MemorySegmentType.THAT),
                                                           that_offset_from_end_frame, self._end_frame) \
               + write_to_address_from_address_minus_value(get_segment_pointer(MemorySegmentType.THIS),
                                                           this_offset_from_end_frame, self._end_frame) \
               + write_to_address_from_address_minus_value(get_segment_pointer(MemorySegmentType.ARGUMENT),
                                                           arg_offset_from_end_frame, self._end_frame) \
               + write_to_address_from_address_minus_value(get_segment_pointer(MemorySegmentType.LOCAL),
                                                           lcl_offset_from_end_frame, self._end_frame) \
               + set_address_from_pointer(ret_addr) + unconditional_jmp()

    def get_call(self, f_name, n_args):
        caller_frame_size = '5'
        ret_label_symbol = 'ret'
        if f_name in self._f_ret_cnt:
            self._f_ret_cnt[f_name] +=1
        else:
            self._f_ret_cnt[f_name] = 1
        ret_addr_label = f_name + '$' + ret_label_symbol + '.' + str(self._f_ret_cnt[f_name])
        return push_from_value(ret_addr_label) \
               + push_from_address(get_segment_pointer(MemorySegmentType.LOCAL)) \
               + push_from_address(get_segment_pointer(MemorySegmentType.ARGUMENT)) \
               + push_from_address(get_segment_pointer(MemorySegmentType.THIS)) \
               + push_from_address(get_segment_pointer(MemorySegmentType.THAT)) \
               + write_to_address_sp_minus_values(get_segment_pointer(MemorySegmentType.ARGUMENT),
                                                  caller_frame_size, n_args) \
               + write_from_sp_to_address(get_segment_pointer(MemorySegmentType.LOCAL)) \
               + self.get_goto(f_name) \
               + self.get_label(ret_addr_label)

    def get_push_basic_segment(self, segment, i):
        return write_from_pointer_plus_value_to_d(i, get_segment_pointer(segment)) + push_from_d()

    def get_pop_basic_segment(self, segment, i):
        return set_pointer_to_pointer_plus_offset(get_segment_pointer(segment), i, self._tmp_address) \
               + pop_to_pointer(self._tmp_address)

    def get_push_const_segment(self, i):
        return write_value_to_d(i) + push_from_d()

    def get_push_static_segment(self, i):
        if self._current_filename is not None:
            return push_from_address(self._current_filename + '.' + i)
        raise InvalidOperation('Current filename should be set before calling this method.')

    def get_pop_static_segment(self, i):
        if self._current_filename is not None:
            return pop_to_address(self._current_filename + '.' + i)
        raise InvalidOperation('Current filename should be set before calling this method.')

    def get_push_temp_segment(self, i):
        return write_to_d_from_added_values_address(self._temp_segment_start_address, i) \
               + push_from_d()

    def get_pop_temp_segment(self, i):
        return set_pointer_to_address_plus_offset(self._temp_segment_start_address, i, self._tmp_address) \
               + pop_to_pointer(self._tmp_address)

    def get_push_pointer_segment(self, i):
        if i == self._this_pointer_symbol:
            instruction = write_to_d_from_address(self._THIS)
        elif i == self._that_pointer_symbol:
            instruction = write_to_d_from_address(self._THAT)
        else:
            raise CommandError
        return instruction + push_from_d()

    def get_pop_pointer_segment(self, i):
        if i == self._this_pointer_symbol:
            instruction = write_from_d_to_address(self._THIS)
        elif i == self._that_pointer_symbol:
            instruction = write_from_d_to_address(self._THAT)
        else:
            raise CommandError
        return pop_to_d() + instruction

    def close_output_file(self):
        self._output_file.close()

    def _write_to_file(self, content):
        self._output_file.write(content)


def get_segment_pointer(segment):
    if segment == MemorySegmentType.LOCAL:
        return 'LCL'
    if segment == MemorySegmentType.ARGUMENT:
        return 'ARG'
    if segment == MemorySegmentType.THIS:
        return 'THIS'
    if segment == MemorySegmentType.THAT:
        return 'THAT'
    raise InvalidValue()


def is_basic_segment(segment):
    return segment == MemorySegmentType.LOCAL \
           or segment == MemorySegmentType.ARGUMENT \
           or segment == MemorySegmentType.THIS \
           or segment == MemorySegmentType.THAT


def is_const_segment(segment):
    return segment == MemorySegmentType.CONSTANT


def is_static_segment(segment):
    return segment == MemorySegmentType.STATIC


def is_temp_segment(segment):
    return segment == MemorySegmentType.TEMP


def is_pointer_segment(segment):
    return segment == MemorySegmentType.POINTER


def is_add(operation):
    return operation == ArithmeticCommandType.ADD


def is_sub(operation):
    return operation == ArithmeticCommandType.SUB


def is_neg(operation):
    return operation == ArithmeticCommandType.NEG


def is_eq(operation):
    return operation == ArithmeticCommandType.EQ


def is_gt(operation):
    return operation == ArithmeticCommandType.GT


def is_lt(operation):
    return operation == ArithmeticCommandType.LT


def is_and(operation):
    return operation == ArithmeticCommandType.AND


def is_or(operation):
    return operation == ArithmeticCommandType.OR


def is_not(operation):
    return operation == ArithmeticCommandType.NOT
