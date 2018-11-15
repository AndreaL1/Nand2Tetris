from os import system
import unittest


class TestVMTranslator(unittest.TestCase):

    def test_seven(self):
        test_name = 'Main'
        test_folder = 'Seven/'
        test = test_folder + test_name + '.jack'
        system("python3 ../JackCompiler.py " + test)
        res_file = test_folder + test_name + '.vm'
        cmp_file = test_folder + 'ExpectedOutput/' + test_name + '.vm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

    def test_convert_to_bin(self):
        test_name = 'Main'
        test_folder = 'ConvertToBin/'
        test = test_folder + test_name + '.jack'
        system("python3 ../JackCompiler.py " + test)
        res_file = test_folder + test_name + '.vm'
        cmp_file = test_folder + 'ExpectedOutput/' + test_name + '.vm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

    def test_square(self):
        test_name = 'Main'
        test_folder = 'Square/'
        test = test_folder + test_name + '.jack'
        system("python3 ../JackCompiler.py " + test)
        res_file = test_folder + test_name + '.vm'
        cmp_file = test_folder + 'ExpectedOutput/' + test_name + '.vm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

        test_name = 'Square'
        test = test_folder + test_name + '.jack'
        system("python3 ../JackCompiler.py " + test)
        res_file = test_folder + test_name + '.vm'
        cmp_file = test_folder + 'ExpectedOutput/' + test_name + '.vm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

        test_name = 'SquareGame'
        test = test_folder + test_name + '.jack'
        system("python3 ../JackCompiler.py " + test)
        res_file = test_folder + test_name + '.vm'
        cmp_file = test_folder + 'ExpectedOutput/' + test_name + '.vm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

    def test_average(self):
        test_name = 'Main'
        test_folder = 'Average/'
        test = test_folder + test_name + '.jack'
        system("python3 ../JackCompiler.py " + test)
        res_file = test_folder + test_name + '.vm'
        cmp_file = test_folder + 'ExpectedOutput/' + test_name + '.vm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

    def test_pong(self):
        test_name = 'Main'
        test_folder = 'Pong/'
        test = test_folder + test_name + '.jack'
        system("python3 ../JackCompiler.py " + test)
        res_file = test_folder + test_name + '.vm'
        cmp_file = test_folder + 'ExpectedOutput/' + test_name + '.vm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

        test_name = 'Ball'
        test = test_folder + test_name + '.jack'
        system("python3 ../JackCompiler.py " + test)
        res_file = test_folder + test_name + '.vm'
        cmp_file = test_folder + 'ExpectedOutput/' + test_name + '.vm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

        test_name = 'Bat'
        test = test_folder + test_name + '.jack'
        system("python3 ../JackCompiler.py " + test)
        res_file = test_folder + test_name + '.vm'
        cmp_file = test_folder + 'ExpectedOutput/' + test_name + '.vm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

        test_name = 'PongGame'
        test = test_folder + test_name + '.jack'
        system("python3 ../JackCompiler.py " + test)
        res_file = test_folder + test_name + '.vm'
        cmp_file = test_folder + 'ExpectedOutput/' + test_name + '.vm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())

    def test_complex_arrays(self):
        test_name = 'Main'
        test_folder = 'ComplexArrays/'
        test = test_folder + test_name + '.jack'
        system("python3 ../JackCompiler.py " + test)
        res_file = test_folder + test_name + '.vm'
        cmp_file = test_folder + 'ExpectedOutput/' + test_name + '.vm'
        with open(res_file) as f1:
            with open(cmp_file) as f2:
                self.assertTrue(f1.read() == f2.read())
