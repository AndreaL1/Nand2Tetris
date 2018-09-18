from Exceptions import InstructionError
from InstructionType import InstructionType


class Code:
    _c_instruction_symbol = '111'
    _a_instruction_symbol = '0'

    def __init__(self, instruction_type, instruction_fields):
        self._instruction_type = instruction_type
        self._instruction_fields = instruction_fields

    def convert_instruction_to_machine_code(self):
        if self._instruction_type == InstructionType.A_INSTRUCTION:
            return self._convert_a_instruction_to_machine_code()
        else:
            return self._convert_c_instruction_to_machine_code()

    def _convert_c_instruction_to_machine_code(self):
        if len(self._instruction_fields) != 3:
            raise InstructionError('Invalid instruction!')
        return self._c_instruction_symbol + self._convert_c_instruction_comp() + \
            self._convert_c_instruction_dest() + self._convert_c_instruction_jmp()

    def _convert_a_instruction_to_machine_code(self):
        a_instruction_value_length = 15
        bin_format_value_start_idx = 2
        value = self._instruction_fields[0]
        if len(self._instruction_fields) != 1:
            raise InstructionError('Invalid instruction!')
        instruction = int(value)
        binary_value = bin(instruction)[bin_format_value_start_idx:]
        zeros = ''.join(['0' for i in range(0, a_instruction_value_length - len(binary_value))])
        return self._a_instruction_symbol + zeros + binary_value

    def _convert_c_instruction_dest(self):
        dest = self._instruction_fields[0]
        if dest == 'null':
            return '000'
        if dest == 'M':
            return '001'
        if dest == 'D':
            return '010'
        if dest == 'MD':
            return '011'
        if dest == 'A':
            return '100'
        if dest == 'AM':
            return '101'
        if dest == 'AD':
            return '110'
        if dest == 'AMD':
            return '111'
        raise InstructionError('Invalid instruction!')

    def _convert_c_instruction_comp(self):
        comp = self._instruction_fields[1]
        if comp == '0':
            return '0101010'
        if comp == '1':
            return '0111111'
        if comp == '-1':
            return '0111010'
        if comp == 'D':
            return '0001100'
        if comp == 'A':
            return '0110000'
        if comp == '!D':
            return '0001101'
        if comp == '!A':
            return '0110001'
        if comp == '-D':
            return '0001111'
        if comp == '-A':
            return '0110011'
        if comp == 'D+1':
            return '0011111'
        if comp == 'A+1':
            return '0110111'
        if comp == 'D-1':
            return '0001110'
        if comp == 'A-1':
            return '0110010'
        if comp == 'D+A':
            return '0000010'
        if comp == 'D-A':
            return '0010011'
        if comp == 'A-D':
            return '0000111'
        if comp == 'D&A':
            return '0000000'
        if comp == 'D|A':
            return '0010101'
        if comp == 'M':
            return '1110000'
        if comp == '!M':
            return '1110001'
        if comp == '-M':
            return '1110011'
        if comp == 'M+1':
            return '1110111'
        if comp == 'M-1':
            return '1110010'
        if comp == 'D+M':
            return '1000010'
        if comp == 'D-M':
            return '1010011'
        if comp == 'M-D':
            return '1000111'
        if comp == 'D&M':
            return '1000000'
        if comp == 'D|M':
            return '1010101'
        raise InstructionError('Invalid instruction!')

    def _convert_c_instruction_jmp(self):
        jmp = self._instruction_fields[2]
        if jmp == '' or jmp == 'null':
            return '000'
        if jmp == 'JGT':
            return '001'
        if jmp == 'JEQ':
            return '010'
        if jmp == 'JGE':
            return '011'
        if jmp == 'JLT':
            return '100'
        if jmp == 'JNE':
            return '101'
        if jmp == 'JLE':
            return '110'
        if jmp == 'JMP':
            return '111'
        raise InstructionError('Invalid instruction!')