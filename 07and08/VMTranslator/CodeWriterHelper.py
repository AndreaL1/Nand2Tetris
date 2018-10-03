_SP = 'SP'


def push_from_address(in_address):
    return write_to_d_from_address(in_address) + push_from_d()


def push_from_value(value):
    return write_value_to_d(value) + push_from_d()


def push_from_d():
    return '@' + _SP + '\nA=M\nM=D\n@' + _SP + '\nM=M+1\n'


def pop_to_pointer(out_pointer):
    return pop_to_d() + write_from_d_to_pointer(out_pointer)


def pop_to_address(out_address):
    return pop_to_d() + write_from_d_to_address(out_address)


def pop_to_d():
    return '@' + _SP + '\nAM=M-1\nD=M\n'


def pop_add_to_d():
    return '@' + _SP + '\nAM=M-1\nD=D+M\n'


def pop_sub_to_d():
    return '@' + _SP + '\nAM=M-1\nD=M-D\n'


def pop_neg_to_d():
    return '@' + _SP + '\nAM=M-1\nD=-M\n'


def pop_and_to_d():
    return '@' + _SP + '\nAM=M-1\nD=D&M\n'


def pop_or_to_d():
    return '@' + _SP + '\nAM=M-1\nD=M|D\n'


def pop_not_to_d():
    return '@' + _SP + '\nAM=M-1\nD=!M\n'


def set_sp_to_arg_plus_one():
    return '@ARG\nD=M+1\n' + write_from_d_to_address(_SP)


def set_sp_to_value(value):
    return write_value_to_d(value) + write_from_d_to_address(_SP)


def set_pointer_to_pointer_plus_offset(original_pointer, offset, pointer):
    return write_value_to_d(offset) + '@' + original_pointer + '\nD=D+M\n' \
           + write_from_d_to_address(pointer)


def set_pointer_to_address_plus_offset(address, offset, pointer):
    return write_value_to_d(address) + '@' + offset + '\nD=D+A\n' \
           + write_from_d_to_address(pointer)


def write_from_pointer_plus_value_to_d(value, pointer):
    return write_value_to_d(value) + '@' + pointer + '\nA=M+D\nD=M\n'


def write_from_d_to_address(address):
    return '@' + address + '\nM=D\n'


def write_from_d_to_pointer(pointer):
    return '@' + pointer + '\nA=M\nM=D\n'


def write_value_to_d(value):
    return '@' + value + '\nD=A\n'


def write_to_d_from_address(address):
    return '@' + address + '\nD=M\n'


def write_to_d_from_added_values_address(value_one, value_two):
    return '@' + value_one + '\nD=A\n' + '@' + value_two + '\nA=D+A\nD=M\n'


def write_to_d_from_pointer(pointer):
    return '@' + pointer + '\nA=M\nD=M\n'


def write_to_d_d_minus_value(value):
    return '@' + value + '\nD=D-A\n'


def write_from_address_to_address(in_address, out_address):
    return write_to_d_from_address(in_address) + write_from_d_to_address(out_address)


def write_from_sp_to_address(address):
    return write_from_address_to_address(_SP, address)


#if in_address_label is None, then the input address is already in D
def write_to_address_from_address_minus_value(out_address, value, in_address_label = None):
    return (write_to_d_from_address(in_address_label) if in_address_label is not None else '') \
           + '@' + value + '\nA=D-A\nD=M\n' + write_from_d_to_address(out_address)


def write_to_d_eq_d_to_zero(label_num):
    return '@CMPTRUE' + str(label_num) + '\nD;JEQ\nD=0\n@SKIPCMPTRUE' + str(label_num) + '\n' \
           + unconditional_jmp() + '(CMPTRUE' + str(label_num) + ')\nD=-1\n(SKIPCMPTRUE' + str(label_num) + ')\n'


def write_to_d_lt_d_to_zero(label_num):
    return '@CMPTRUE' + str(label_num) + '\nD;JLT\nD=0\n@SKIPCMPTRUE' + str(label_num) + '\n' \
           + unconditional_jmp() + '(CMPTRUE' + str(label_num) + ')\nD=-1\n(SKIPCMPTRUE' + str(label_num) + ')\n'


def write_to_d_gt_d_to_zero(label_num):
    return '@CMPTRUE' + str(label_num) + '\nD;JGT\nD=0\n@SKIPCMPTRUE' + str(label_num) + '\n' \
           + unconditional_jmp() + '(CMPTRUE' + str(label_num) + ')\nD=-1\n(SKIPCMPTRUE' + str(label_num) + ')\n'


def unconditional_jmp():
    return '0;JMP\n'


def set_address(address):
    return '@' + address + '\n'


def set_address_from_pointer(pointer):
    return '@' + pointer + '\nA=M\n'


def jmp_not_equal():
    return 'D;JNE\n'


def write_label(label):
    return '(' + label + ')\n'


def write_to_address_sp_minus_values(address, value_one, value_two = None):
    return write_to_d_from_address(_SP) + write_to_d_d_minus_value(value_one) \
           + (write_to_d_d_minus_value(value_two) if value_two is not None else '') \
           + write_from_d_to_address(address)
