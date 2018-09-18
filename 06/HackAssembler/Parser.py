from InstructionType import InstructionType


class Parser:
    _comment_sign = '//'

    def __init__(self, input_file, symbolTable):
        self._set_instructions(input_file)
        self._current_instruction_idx = -1
        self._symbolTable = symbolTable
        self._n = 16

    def add_labels_to_symbol_table(self):
        temp_current_instruction_idx = self._current_instruction_idx
        self._current_instruction_idx = 0
        while self.has_more_instructions():
            if self._instruction_is_label():
                label = self._get_label_from_instruction()
                if not self._symbolTable.contains(label):
                    self._symbolTable.set_symbol(label, self._current_instruction_idx)
                del self._instructions[self._current_instruction_idx]
            else:
                self.advance()

        self._current_instruction_idx = temp_current_instruction_idx

    def get_instruction(self):
        return self._instructions[self._current_instruction_idx]

    def has_more_instructions(self):
        return self._current_instruction_idx < len(self._instructions) - 1

    def advance(self):
        self._current_instruction_idx += 1

    def instruction_type(self):
        if self.get_instruction()[0] == '@':
            return InstructionType.A_INSTRUCTION
        return InstructionType.C_INSTRUCTION

    def get_instruction_fields(self):
        if self.instruction_type() == InstructionType.A_INSTRUCTION:
            return self._get_a_instruction_fields()
        else:
            return self._get_c_instruction_fields()

    def _instruction_is_label(self):
        instr = self.get_instruction()
        if instr[0] == '(' and instr[len(instr) - 1] == ')':
            return True
        return False

    def _get_label_from_instruction(self):
        instr = self.get_instruction()
        return instr[instr.find('(') + 1 : instr.find(')')]

    def _get_a_instruction_fields(self):
        value = self.get_instruction()[1:]
        if value.isdigit():
            return [value]
        elif self._symbolTable.contains(value):
            return [self._symbolTable.get_value(value)]
        else:
            self._symbolTable.set_symbol(value, self._n)
            self._n += 1
            return [self._symbolTable.get_value(value)]

    def _get_c_instruction_fields(self):
        return [self._get_c_instruction_destination_string(), self._get_c_instruction_computation_string(), \
               self._get_c_instruction_jump_string()]

    def _get_c_instruction_destination_string(self):
        current_instruction = self.get_instruction()
        if '=' in current_instruction:
            return current_instruction[0: current_instruction.find('=')]
        else:
            return 'null'

    def _get_c_instruction_computation_string(self):
        current_instruction = self.get_instruction()
        if ';' in current_instruction:
            return current_instruction[current_instruction.find('=') + 1: current_instruction.find(';')]
        else:
            return current_instruction[current_instruction.find('=') + 1:]

    def _get_c_instruction_jump_string(self):
        current_instruction = self.get_instruction()
        if ';' in self.get_instruction():
            return current_instruction[current_instruction.find(';') + 1:]
        else:
            return ''

    def _set_instructions(self, file):
        file_content = self._read_file(file)
        self._instructions = self._get_raw_instructions(file_content)

    def _get_raw_instructions(self, content):
        return self._remove_empty_lines(self._remove_comments(self._strip_content(content)))

    def _read_file(self, file):
        with open(file) as f:
            return f.readlines()

    def _remove_comments(self, content):
        return [line[:line.find(self._comment_sign)] if self._comment_sign in line else line for line in content]

    def _strip_content(self, content):
        return [x.strip().replace(" ", "") for x in content]

    def _remove_empty_lines(self, content):
        return [line for line in content if len(line) > 0]

