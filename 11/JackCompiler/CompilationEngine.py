import xml.etree.ElementTree as ET

from ArithmeticCommandType import *
from JackGrammar import *
from JackTokenizer import JackTokenizer
from MemorySegmentType import MemorySegmentType
import OS
from SymbolTable import SymbolTable
from VMWriter import VMWriter

class CompilationEngine:
    def __init__(self, tokenizer: JackTokenizer, vm_writer: VMWriter):
        self._tokenizer = tokenizer
        self._vm_writer = vm_writer
        self._label_idx = -1
        self._compile_class()

    def _compile_class(self):
        self._symbol_table = SymbolTable()

        self._tokenizer.advance() # class
        self._tokenizer.advance() # className
        self._class_name = self._tokenizer.get_token()
        self._tokenizer.advance() # left curly parenthesis
        self._tokenizer.advance()
        while is_class_var_type(self._tokenizer.get_token()):
            self._compile_class_variable_declaration()  # classVarDec
            self._tokenizer.advance() # skip semicolon

        while not is_right_curly_parenthesis(self._tokenizer.get_token()):
            self._compile_subroutine() # subroutine
            self._tokenizer.advance() # right curly parenthesis

    def _compile_class_variable_declaration(self):
        var_identifier_type = get_identifier_type_from_str(self._tokenizer.get_token())
        self._tokenizer.advance()  # skip static or field
        var_type = self._tokenizer.get_token()
        self._tokenizer.advance()
        self._add_new_var_to_symbol_table(var_type, var_identifier_type)  # varName
        self._tokenizer.advance()
        while is_comma(self._tokenizer.get_token()):
            self._tokenizer.advance()  # skip comma
            self._add_new_var_to_symbol_table(var_type, var_identifier_type)  # varName
            self._tokenizer.advance()

    def _compile_subroutine(self):
        self._symbol_table.start_subroutine()

        #subroutine declaration
        subroutine_type = self._tokenizer.get_token()  # constructor or function or method
        self._tokenizer.advance() # type
        self._tokenizer.advance() # subroutineName
        subroutine_name = self._class_name + '.' + self._tokenizer.get_token()
        self._tokenizer.advance()  # left parenthesis
        if is_method(subroutine_type):
            self._add_new_var_to_symbol_table(self._class_name, IdentifierType.ARG)
        self._compile_parameter_list()
        self._tokenizer.advance()  # skip right parenthesis

        # subroutine body
        self._tokenizer.advance() # skip left curly parenthesis
        local_num = 0
        while is_var_dec(self._tokenizer.get_token()):
            local_num += self._compile_variable_declaration()  # varDec
            self._tokenizer.advance() # skip semicolon
        self._vm_writer.write_function(subroutine_name, local_num)
        if is_constructor(subroutine_type):
            self._compile_constructor_pointer_segment_setup(self._symbol_table.var_count(IdentifierType.FIELD))
        elif is_method(subroutine_type):
            self._compile_method_pointer_segment_setup()
        self._compile_statements()  # statements

    def _compile_parameter_list(self):
        self._tokenizer.advance() # skip left parenthesis
        if not is_right_parenthesis(self._tokenizer.get_token()):
            var_type = self._tokenizer.get_token()
            self._tokenizer.advance()  # varName
            self._add_new_var_to_symbol_table(var_type, IdentifierType.ARG)
            self._tokenizer.advance()
            while not is_right_parenthesis(self._tokenizer.get_token()):
                self._tokenizer.advance()  # type
                var_type = self._tokenizer.get_token()
                self._tokenizer.advance()  # varName
                self._add_new_var_to_symbol_table(var_type, IdentifierType.ARG)
                self._tokenizer.advance()


    def _compile_variable_declaration(self):
        var_num = 1
        self._tokenizer.advance() # skip var
        var_type = self._tokenizer.get_token()
        self._tokenizer.advance()  # varName
        self._add_new_var_to_symbol_table(var_type, IdentifierType.LOCAL)
        self._tokenizer.advance()
        while is_comma(self._tokenizer.get_token()):
            var_num +=1
            self._tokenizer.advance()  # varName
            self._add_new_var_to_symbol_table(var_type, IdentifierType.LOCAL)
            self._tokenizer.advance()
        return var_num

    def _compile_statements(self):
        current_token = self._tokenizer.get_token()
        while (True):
            if is_let(current_token):
                self._compile_let()
            elif is_if(current_token):
                self._compile_if()
            elif is_while(current_token):
                self._compile_while()
            elif is_do(current_token):
                self._compile_do()
            elif is_return(current_token):
                self._compile_return()
            else:
                break
            current_token = self._tokenizer.get_token()

    def _compile_do(self):
        self._tokenizer.advance() # skip do
        self._compile_subroutine_call()  # subroutine call
        self._tokenizer.advance()  # skip semicolon
        self._vm_writer.write_pop(MemorySegmentType.TEMP, '0')

    def _compile_let(self):
        self._tokenizer.advance() # skip let
        segment = self._get_var_segment()
        var_idx = self._symbol_table.index_of(self._tokenizer.get_token())
        current_token = self._tokenizer.get_token()
        self._tokenizer.advance()
        next_token = self._tokenizer.get_token()
        if is_left_square_parenthesis(next_token):  # varName[expression]
            self._vm_writer.write_push(self._get_var_segment(current_token), self._symbol_table.index_of(current_token))
            self._compile_expression_with_surrounding_square_parenthesis()  # [expression]
            self._vm_writer.write_arithmetic(ArithmeticCommandType.ADD)
            self._tokenizer.advance() # skip equal
            self._compile_expression()  # expression
            self._vm_writer.write_pop(MemorySegmentType.TEMP, '0')
            self._vm_writer.write_pop(MemorySegmentType.POINTER, '1')
            self._vm_writer.write_push(MemorySegmentType.TEMP, '0')
            self._vm_writer.write_pop(MemorySegmentType.THAT, '0')
        else:
            self._tokenizer.advance()  # skip equal
            self._compile_expression()  # expression
            self._vm_writer.write_pop(segment, var_idx)
        self._tokenizer.advance()  # skip semicolon

    def _compile_while(self):
        self._tokenizer.advance() # skip while
        start_label = self._get_new_label()
        self._vm_writer.write_label(start_label)
        self._compile_expression_with_surrounding_parenthesis() # (expression)
        self._vm_writer.write_arithmetic(ArithmeticCommandType.NOT)
        end_label = self._get_new_label()
        self._vm_writer.write_if_goto(end_label)
        self._compile_statements_with_surrounding_parenthesis() # {statements}
        self._vm_writer.write_goto(start_label)
        self._vm_writer.write_label(end_label)

    def _compile_return(self):
        self._tokenizer.advance()  # return
        if not is_semicolon(self._tokenizer.get_token()):
            self._compile_expression()
        else:
            self._vm_writer.write_push(MemorySegmentType.CONSTANT, '0')
        self._tokenizer.advance()  # semicolon
        self._vm_writer.write_return()

    def _compile_if(self):
        self._tokenizer.advance()  # skip if
        self._compile_expression_with_surrounding_parenthesis()  # (expression)
        self._vm_writer.write_arithmetic(ArithmeticCommandType.NOT)
        if_not_label = self._get_new_label()
        self._vm_writer.write_if_goto(if_not_label)
        self._compile_statements_with_surrounding_parenthesis()  # {statements}
        if is_else(self._tokenizer.get_token()):
            skip_else = self._get_new_label()
            self._vm_writer.write_goto(skip_else)
            self._tokenizer.advance()  # else
            self._vm_writer.write_label(if_not_label)
            self._compile_statements_with_surrounding_parenthesis()  # {statements}
            self._vm_writer.write_label(skip_else)
        else:
            self._vm_writer.write_label(if_not_label)

    def _compile_expression(self):
        self._compile_term()
        operator_list = []
        while is_operation(self._tokenizer.get_token()):
            operator_list.append(self._tokenizer.get_token())  # operator
            self._tokenizer.advance()
            self._compile_term()
        self._compile_operators(operator_list)

    def _compile_term(self):
        if is_left_parenthesis(self._tokenizer.get_token()):  # (expression)
            self._compile_expression_with_surrounding_parenthesis()
        elif is_unary_operation(self._tokenizer.get_token()):  # unaryOp term
            operator = self._tokenizer.get_token()
            self._tokenizer.advance()
            self._compile_term()  # term
            self._compile_operators(operator, True)  # unaryOp
        else:
            if self._tokenizer.token_type() != TokenType.IDENTIFIER:  # integerConstant/stringConstant/keywordConstant
                if self._tokenizer.token_type() == TokenType.INTEGER_CONSTANT:
                    self._compile_integer_constant()
                    self._tokenizer.advance()
                elif self._tokenizer.token_type() == TokenType.STRING_CONSTANT:
                    self._compile_string_constant()
                    self._tokenizer.advance()
                elif self._tokenizer.token_type() == TokenType.KEYWORD:
                    self._compile_keyword()
                    self._tokenizer.advance()
            else:
                current_token = self._tokenizer.get_token()
                self._tokenizer.advance()
                next_token = self._tokenizer.get_token()

                if is_left_square_parenthesis(next_token):  # varName[expression]
                    self._vm_writer.write_push(self._get_var_segment(current_token), self._symbol_table.index_of(current_token))
                    self._compile_expression_with_surrounding_square_parenthesis()  # [expression]
                    self._vm_writer.write_arithmetic(ArithmeticCommandType.ADD)
                    self._vm_writer.write_pop(MemorySegmentType.POINTER, '1')
                    self._vm_writer.write_push(MemorySegmentType.THAT, '0')
                elif (not is_left_parenthesis(next_token)) & (not is_dot(next_token)):
                    self._vm_writer.write_push(self._get_var_segment(current_token), self._symbol_table.index_of(current_token))
                else:
                    self._compile_subroutine_call(current_token)

    def _compile_expression_list(self):
        num_expressions = 0
        if not is_right_parenthesis(self._tokenizer.get_token()):
            num_expressions += 1
            self._compile_expression()  # expression
            while is_comma(self._tokenizer.get_token()):
                self._tokenizer.advance()  # comma
                self._compile_expression()  # expression
                num_expressions += 1
        return num_expressions

    def _compile_statements_with_surrounding_parenthesis(self):
        self._tokenizer.advance() # skip left curly parenthesis
        self._compile_statements() # statements
        self._tokenizer.advance()  # skip right curly parenthesis

    def _compile_expression_with_surrounding_square_parenthesis(self):
        self._tokenizer.advance() # skip left square parenthesis
        self._compile_expression()  # expression
        self._tokenizer.advance()  # skip right square parenthesis

    def _compile_expression_with_surrounding_parenthesis(self):
        self._tokenizer.advance()  # skip left parenthesis
        self._compile_expression()  # expression
        self._tokenizer.advance()  # skip right parenthesis

    def _compile_expression_list_with_surrounding_parenthesis(self):
        self._tokenizer.advance()  # skip left parenthesis
        num_expressions = self._compile_expression_list()  # expression list
        self._tokenizer.advance()  # skip right parenthesis
        return num_expressions

    def _compile_subroutine_call(self, current_token=None):
        f_name = ''
        n_args = 0
        if current_token is None:
            current_token = self._tokenizer.get_token()  # className or varName or subroutineName
            self._tokenizer.advance()
        if is_dot(self._tokenizer.get_token()):
            if self._symbol_table.is_var(current_token):
                f_name += self._symbol_table.type_of(current_token)
                self._vm_writer.write_push(self._get_var_segment(current_token), self._symbol_table.index_of(current_token))
                n_args +=1
            else:
                f_name += current_token
            f_name += self._tokenizer.get_token()  # dot
            self._tokenizer.advance()
            f_name += self._tokenizer.get_token() # subroutineName
            self._tokenizer.advance()
        else:
            f_name = self._class_name + '.'
            f_name += current_token # subroutineName
            n_args += 1 # this
            self._vm_writer.write_push(MemorySegmentType.POINTER, 0)

        n_args += self._compile_expression_list_with_surrounding_parenthesis()  # (expression list)
        self._vm_writer.write_call(f_name, n_args)

    def _compile_operators(self, operator_list, unary=False):
        for op in operator_list:
            if op == '*':
                self._vm_writer.write_call(*OS.get_multiply())
            if op == '/':
                self._vm_writer.write_call(*OS.get_divide())
            elif op == '+':
                self._vm_writer.write_arithmetic(ArithmeticCommandType.ADD)
            elif (op == '-') & (unary == False):
                self._vm_writer.write_arithmetic(ArithmeticCommandType.SUB)
            elif op == '-':
                self._vm_writer.write_arithmetic(ArithmeticCommandType.NEG)
            elif op == '=':
                self._vm_writer.write_arithmetic(ArithmeticCommandType.EQ)
            elif op == '>':
                self._vm_writer.write_arithmetic(ArithmeticCommandType.GT)
            elif op == '<':
                self._vm_writer.write_arithmetic(ArithmeticCommandType.LT)
            elif op == '&':
                self._vm_writer.write_arithmetic(ArithmeticCommandType.AND)
            elif op == '|':
                self._vm_writer.write_arithmetic(ArithmeticCommandType.OR)
            elif op == '~':
                self._vm_writer.write_arithmetic(ArithmeticCommandType.NOT)

    def _compile_keyword(self):
        token = self._tokenizer.get_token()
        if is_true(token):
            self._vm_writer.write_push(MemorySegmentType.CONSTANT, 1)
            self._vm_writer.write_arithmetic(ArithmeticCommandType.NEG)
        elif is_false(token):
            self._vm_writer.write_push(MemorySegmentType.CONSTANT, 0)
        elif is_null(token):
            self._vm_writer.write_push(MemorySegmentType.CONSTANT, 0)
        elif token == 'this':
            self._vm_writer.write_push(MemorySegmentType.POINTER, 0)

    def _compile_constructor_pointer_segment_setup(self, num_words):
        if num_words != 0:
            self._vm_writer.write_push(MemorySegmentType.CONSTANT, num_words)
        self._vm_writer.write_call(*OS.get_alloc())
        self._vm_writer.write_pop(MemorySegmentType.POINTER, 0)

    def _compile_method_pointer_segment_setup(self):
        self._vm_writer.write_push(MemorySegmentType.ARGUMENT, 0)
        self._vm_writer.write_pop(MemorySegmentType.POINTER, 0)

    def _compile_integer_constant(self):
        self._vm_writer.write_push(MemorySegmentType.CONSTANT, self._tokenizer.get_token())

    def _compile_string_constant(self):
        string_const = self._tokenizer.get_token()
        self._vm_writer.write_push(MemorySegmentType.CONSTANT, len(string_const))
        self._vm_writer.write_call(*OS.get_string_new())
        for character in string_const:
            self._vm_writer.write_push(MemorySegmentType.CONSTANT, ord(character))
            self._vm_writer.write_call(*OS.get_string_append())

    def _get_var_segment(self, token=None):
        if token is None:
            token = self._tokenizer.get_token()
        identifier_type = self._symbol_table.kind_of(token)
        if identifier_type == IdentifierType.LOCAL:
            return MemorySegmentType.LOCAL
        elif identifier_type == IdentifierType.STATIC:
            return MemorySegmentType.STATIC
        elif identifier_type == IdentifierType.ARG:
            return MemorySegmentType.ARGUMENT
        elif identifier_type == IdentifierType.FIELD:
            return MemorySegmentType.THIS

    def _add_new_var_to_symbol_table(self, var_type, var_identifier_type):
        self._symbol_table.define(self._tokenizer.get_token(), var_type, var_identifier_type)

    def _get_new_label(self):
        self._label_idx +=1
        return 'L' + str(self._label_idx)
