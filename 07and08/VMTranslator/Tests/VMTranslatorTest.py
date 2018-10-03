import unittest

from VMTranslator import *


class TestVMTranslator(unittest.TestCase):

    memory_access_path = 'Tests/MemoryAccess/'
    stack_arith_path = 'Tests/StackArithmetic/'

    def test_non_existent_input_file(self):
        non_existent_file = self.stack_arith_path + 'sth.asm'
        out_file = 'out.txt'
        with self.assertRaises(IOError):
            VMTranslator(non_existent_file, out_file, False)

    def test_non_existent_output_file(self):
        test_name = 'StackTest'
        test_folder = self.stack_arith_path + test_name + '/'
        test = test_folder + test_name + '.vm'
        out_file = 'sth/out.txt'
        with self.assertRaises(IOError):
            VMTranslator(test, out_file, False)
