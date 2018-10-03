from os import system
import unittest


class TestVMTranslator(unittest.TestCase):

    memory_access_path = 'MemoryAccess/'
    stack_arith_path = 'StackArithmetic/'
    program_flow_path = 'ProgramFlow/'
    fun_calls_path = 'FunctionCalls/'

    def test_basic(self):
        test_name = 'BasicTest'
        test_folder = self.memory_access_path + test_name + '/'
        test = test_folder + test_name + '.vm'
        system("python ../VMTranslator.py " + test)
        res_file = test_folder + test_name + '.asm'
        cmp_file = test_folder + test_name + '_corr.asm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

    def test_pointer(self):
        test_name = 'PointerTest'
        test_folder = self.memory_access_path + test_name + '/'
        test = test_folder + test_name + '.vm'
        system("python ../VMTranslator.py " + test)
        res_file = test_folder + test_name + '.asm'
        cmp_file = test_folder + test_name + '_corr.asm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

    def test_static(self):
        test_name = 'StaticTest'
        test_folder = self.memory_access_path + test_name + '/'
        test = test_folder + test_name + '.vm'
        system("python ../VMTranslator.py " + test)
        res_file = test_folder + test_name + '.asm'
        cmp_file = test_folder + test_name + '_corr.asm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

    def test_simple_add(self):
        test_name = 'SimpleAdd'
        test_folder = self.stack_arith_path + test_name + '/'
        test = test_folder + test_name + '.vm'
        system("python ../VMTranslator.py " + test)
        res_file = test_folder + test_name + '.asm'
        cmp_file = test_folder + test_name + '_corr.asm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

    def test_stack(self):
        test_name = 'StackTest'
        test_folder = self.stack_arith_path + test_name + '/'
        test = test_folder + test_name + '.vm'
        system("python ../VMTranslator.py " + test)
        res_file = test_folder + test_name + '.asm'
        cmp_file = test_folder + test_name + '_corr.asm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

    def test_fibonacci(self):
        test_name = 'FibonacciSeries'
        test_folder = self.program_flow_path + test_name + '/'
        test = test_folder + test_name + '.vm'
        system("python ../VMTranslator.py " + test)
        res_file = test_folder + test_name + '.asm'
        cmp_file = test_folder + test_name + '_corr.asm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

    def test_basic_loop(self):
        test_name = 'BasicLoop'
        test_folder = self.program_flow_path + test_name + '/'
        test = test_folder + test_name + '.vm'
        system("python ../VMTranslator.py " + test)
        res_file = test_folder + test_name + '.asm'
        cmp_file = test_folder + test_name + '_corr.asm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

    def test_simple_fun(self):
        test_name = 'SimpleFunction'
        test_folder = self.fun_calls_path + test_name + '/'
        test = test_folder + test_name + '.vm'
        system("python ../VMTranslator.py " + test)
        res_file = test_folder + test_name + '.asm'
        cmp_file = test_folder + test_name + '_corr.asm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

    def test_nested_call(self):
        test_name = 'NestedCall'
        test_folder = self.fun_calls_path + test_name + '/'
        system("python ../VMTranslator.py " + test_folder)
        res_file = test_folder + test_name + '.asm'
        cmp_file = test_folder + test_name + '_corr.asm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

    def test_fibonacci_element(self):
        test_name = 'FibonacciElement'
        test_folder = self.fun_calls_path + test_name + '/'
        system("python ../VMTranslator.py " + test_folder)
        res_file = test_folder + test_name + '.asm'
        cmp_file = test_folder + test_name + '_corr.asm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

    def test_statics_test(self):
        test_name = 'StaticsTest'
        test_folder = self.fun_calls_path + test_name + '/'
        system("python ../VMTranslator.py " + test_folder)
        res_file = test_folder + test_name + '.asm'
        cmp_file = test_folder + test_name + '_corr.asm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())
