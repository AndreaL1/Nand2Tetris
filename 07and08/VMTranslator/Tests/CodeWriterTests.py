import unittest
from CodeWriter import CodeWriter
from MemorySegmentType import MemorySegmentType

class TestCodeWriter(unittest.TestCase):
    def test_push_local(self):
        code_writer = CodeWriter()
        i = '5'
        segment = MemorySegmentType.LOCAL
        segment_pointer = 'LCL'
        cmd = '@' + i + '\nD=A\n@' + segment_pointer + '\nA=M+D\nD=M\n'
        cmd += '@SP\nA=M\nM=D\n'
        cmd += '@SP\nM=M+1\n'
        self.assertEqual(code_writer.get_push(segment, i), cmd)

    def test_push_argument(self):
        code_writer = CodeWriter()
        i = '5'
        segment = MemorySegmentType.ARGUMENT
        segment_pointer = 'ARG'
        cmd = '@' + i + '\nD=A\n@' + segment_pointer + '\nA=M+D\nD=M\n'
        cmd += '@SP\nA=M\nM=D\n'
        cmd += '@SP\nM=M+1\n'
        self.assertEqual(code_writer.get_push(segment, i), cmd)

    def test_pop_local(self):
        code_writer = CodeWriter()
        i = '5'
        segment = MemorySegmentType.LOCAL
        segment_pointer = 'LCL'
        cmd = '@' + i + '\nD=A\n@' + segment_pointer + '\nD=D+M\n@addr\nM=D\n'
        cmd += '@SP\nAM=M-1\n'
        cmd += 'D=M\n@addr\nA=M\nM=D\n'
        self.assertEqual(code_writer.get_pop(segment, i), cmd)

    def test_pop_argument(self):
        code_writer = CodeWriter()
        i = '5'
        segment = MemorySegmentType.ARGUMENT
        segment_pointer = 'ARG'
        cmd = '@' + i + '\nD=A\n@' + segment_pointer + '\nD=D+M\n@addr\nM=D\n'
        cmd += '@SP\nAM=M-1\n'
        cmd += 'D=M\n@addr\nA=M\nM=D\n'
        self.assertEqual(code_writer.get_pop(segment, i), cmd)

    def test_push_const(self):
        code_writer = CodeWriter()
        i = '5'
        segment = MemorySegmentType.CONSTANT
        cmd = '@' + i + '\n'
        cmd += 'D=A\n'
        cmd += '@SP\n'
        cmd += 'A=M\n'
        cmd += 'M=D\n'
        cmd += '@SP\n'
        cmd += 'M=M+1\n'
        self.assertEqual(code_writer.get_push(segment, i), cmd)

    def test_push_static(self):
        code_writer = CodeWriter()
        filename = 'filename1'
        code_writer.set_current_filename(filename)
        i = '5'
        segment = MemorySegmentType.STATIC
        cmd = '@' + filename + '.' + i + '\nD=M\n@SP\nA=M\nM=D\n'
        cmd += '@SP\nM=M+1\n'
        self.assertEqual(code_writer.get_push(segment, i), cmd)

    def test_pop_static(self):
        code_writer = CodeWriter()
        filename = 'filename1'
        code_writer.set_current_filename(filename)
        i = '5'
        segment = MemorySegmentType.STATIC
        cmd = '@SP\nAM=M-1\n'
        cmd += 'D=M\n@' + filename + '.' + i + '\nM=D\n'
        self.assertEqual(code_writer.get_pop(segment, i), cmd)

    def test_push_temp(self):
        code_writer = CodeWriter()
        i = '2'
        segment = MemorySegmentType.TEMP
        start_address = '5'
        cmd = '@' + start_address + '\nD=A\n@' + i + '\nA=D+A\nD=M\n'
        cmd += '@SP\nA=M\nM=D\n'
        cmd += '@SP\nM=M+1\n'
        self.assertEqual(code_writer.get_push(segment, i), cmd)

    def test_pop_temp(self):
        code_writer = CodeWriter()
        i = '2'
        segment = MemorySegmentType.TEMP
        start_address = '5'
        cmd = '@' + start_address + '\nD=A\n@' + i + '\nD=D+A\n@addr\nM=D\n'
        cmd += '@SP\nAM=M-1\n'
        cmd += 'D=M\n@addr\nA=M\nM=D\n'
        self.assertEqual(code_writer.get_pop(segment, i), cmd)

    def test_push_this_pointer_symbol(self):
        code_writer = CodeWriter()
        i = '0'
        segment = MemorySegmentType.POINTER
        cmd = '@THIS\nD=M\n@SP\nA=M\nM=D\n'
        cmd += '@SP\nM=M+1\n'
        self.assertEqual(code_writer.get_push(segment, i), cmd)

    def test_push_that_pointer_symbol(self):
        code_writer = CodeWriter()
        i = '1'
        segment = MemorySegmentType.POINTER
        cmd = '@THAT\nD=M\n@SP\nA=M\nM=D\n'
        cmd += '@SP\nM=M+1\n'
        self.assertEqual(code_writer.get_push(segment, i), cmd)

    def test_pop_this_pointer_symbol(self):
        code_writer = CodeWriter()
        i = '0'
        segment = MemorySegmentType.POINTER
        cmd = '@SP\nAM=M-1\n'
        cmd += 'D=M\n@THIS\nM=D\n'
        self.assertEqual(code_writer.get_pop(segment, i), cmd)

    def test_pop_that_pointer_symbol(self):
        code_writer = CodeWriter()
        i = '1'
        segment = MemorySegmentType.POINTER
        cmd = '@SP\nAM=M-1\n'
        cmd += 'D=M\n@THAT\nM=D\n'
        self.assertEqual(code_writer.get_pop(segment, i), cmd)

    def test_add(self):
        code_writer = CodeWriter()
        cmd = '@SP\nAM=M-1\n'
        cmd += 'D=M\n'
        cmd += '@SP\nAM=M-1\n'
        cmd += 'D=D+M\n'
        cmd += '@SP\nA=M\nM=D\n'
        cmd += '@SP\nM=M+1\n'
        self.assertEqual(code_writer.get_add(), cmd)

    def test_sub(self):
        code_writer = CodeWriter()
        cmd = '@SP\nAM=M-1\n'
        cmd += 'D=M\n'
        cmd += '@SP\nAM=M-1\n'
        cmd += 'D=M-D\n'
        cmd += '@SP\nA=M\nM=D\n'
        cmd += '@SP\nM=M+1\n'
        self.assertEqual(code_writer.get_sub(), cmd)

    def test_neg(self):
        code_writer = CodeWriter()
        cmd = '@SP\nAM=M-1\n'
        cmd += 'D=-M\n'
        cmd += '@SP\nA=M\nM=D\n'
        cmd += '@SP\nM=M+1\n'
        self.assertEqual(code_writer.get_neg(), cmd)

    def test_and(self):
        code_writer = CodeWriter()
        cmd = '@SP\nAM=M-1\n'
        cmd += 'D=M\n'
        cmd += '@SP\nAM=M-1\n'
        cmd += 'D=D&M\n'
        cmd += '@SP\nA=M\nM=D\n'
        cmd += '@SP\nM=M+1\n'
        self.assertEqual(code_writer.get_and(), cmd)

    def test_or(self):
        code_writer = CodeWriter()
        cmd = '@SP\nAM=M-1\n'
        cmd += 'D=M\n'
        cmd += '@SP\nAM=M-1\n'
        cmd += 'D=M|D\n'
        cmd += '@SP\nA=M\nM=D\n'
        cmd += '@SP\nM=M+1\n'
        self.assertEqual(code_writer.get_or(), cmd)

    def test_not(self):
        code_writer = CodeWriter()
        cmd = '@SP\nAM=M-1\n'
        cmd += 'D=!M\n'
        cmd += '@SP\nA=M\nM=D\n'
        cmd += '@SP\nM=M+1\n'
        self.assertEqual(code_writer.get_not(), cmd)

    def test_eq(self):
        code_writer = CodeWriter()
        cmd = '@SP\nAM=M-1\n'
        cmd += 'D=M\n'
        cmd += '@SP\nAM=M-1\n'
        cmd += 'D=M-D\n'
        cmd += '@CMPTRUE0\n'
        cmd += 'D;JEQ\n'
        cmd += 'D=0\n@SKIPCMPTRUE0\n0;JMP\n'
        cmd += '(CMPTRUE0)\n'
        cmd += 'D=-1\n'
        cmd += '(SKIPCMPTRUE0)\n'
        cmd += '@SP\nA=M\nM=D\n'
        cmd += '@SP\nM=M+1\n'
        self.assertEqual(code_writer.get_eq(), cmd)

    def test_lt(self):
        code_writer = CodeWriter()
        cmd = '@SP\nAM=M-1\n'
        cmd += 'D=M\n'
        cmd += '@SP\nAM=M-1\n'
        cmd += 'D=M-D\n'
        cmd += '@CMPTRUE0\n'
        cmd += 'D;JLT\n'
        cmd += 'D=0\n@SKIPCMPTRUE0\n0;JMP\n'
        cmd += '(CMPTRUE0)\n'
        cmd += 'D=-1\n'
        cmd += '(SKIPCMPTRUE0)\n'
        cmd += '@SP\nA=M\nM=D\n'
        cmd += '@SP\nM=M+1\n'
        self.assertEqual(code_writer.get_lt(), cmd)

    def test_gt(self):
        code_writer = CodeWriter()
        cmd = '@SP\nAM=M-1\n'
        cmd += 'D=M\n'
        cmd += '@SP\nAM=M-1\n'
        cmd += 'D=M-D\n'
        cmd += '@CMPTRUE0\n'
        cmd += 'D;JGT\n'
        cmd += 'D=0\n@SKIPCMPTRUE0\n0;JMP\n'
        cmd += '(CMPTRUE0)\n'
        cmd += 'D=-1\n'
        cmd += '(SKIPCMPTRUE0)\n'
        cmd += '@SP\nA=M\nM=D\n'
        cmd += '@SP\nM=M+1\n'
        self.assertEqual(code_writer.get_gt(), cmd)

    def test_label(self):
        code_writer = CodeWriter()
        label = 'LOOP'
        cmd = '(' + label + ')\n'
        self.assertEqual(code_writer.get_label(label), cmd)

    def test_goto(self):
        code_writer = CodeWriter()
        label = 'LOOP'
        cmd = '@' + label + '\n0;JMP\n'
        self.assertEqual(code_writer.get_goto(label), cmd)

    def test_function(self):
        code_writer = CodeWriter()
        f_name = 'file.foo'
        num_vars = 3
        cmd = '(' + f_name + ')\n'
        i = '0'
        push_cmd = '@' + i + '\n'
        push_cmd += 'D=A\n'
        push_cmd += '@SP\n'
        push_cmd += 'A=M\n'
        push_cmd += 'M=D\n'
        push_cmd += '@SP\n'
        push_cmd += 'M=M+1\n'
        cmd += push_cmd * num_vars
        self.assertEqual(code_writer.get_function(f_name, num_vars), cmd)

    def test_return(self):
        code_writer = CodeWriter()
        cmd = '@LCL\nD=M\n@endFrame\nM=D\n@5\nA=D-A\nD=M\n@retAddr\nM=D\n'
        cmd += '@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n'
        cmd += '@ARG\nD=M+1\n@SP\nM=D\n'
        cmd += '@endFrame\nD=M\n@1\nA=D-A\nD=M\n@THAT\nM=D\n'
        cmd += '@endFrame\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D\n'
        cmd += '@endFrame\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D\n'
        cmd += '@endFrame\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n'
        cmd += '@retAddr\nA=M\n0;JMP\n'
        self.assertEqual(code_writer.get_return(), cmd)

    def test_call(self):
        code_writer = CodeWriter()
        f_name = 'fun'
        n_args = '3'
        ret_addr = f_name + '$ret.1'
        cmd = '@' + ret_addr + '\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        cmd += '@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        cmd += '@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        cmd += '@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        cmd += '@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        cmd += '@SP\nD=M\n@5\nD=D-A\n@' + n_args + '\nD=D-A\n@ARG\nM=D\n'
        cmd += '@SP\nD=M\n@LCL\nM=D\n'
        cmd += '@' + f_name + '\n0;JMP\n'
        cmd += '(' + ret_addr + ')\n'
        self.assertEqual(code_writer.get_call(f_name, n_args), cmd)


if __name__ == '__main__':
    unittest.main()