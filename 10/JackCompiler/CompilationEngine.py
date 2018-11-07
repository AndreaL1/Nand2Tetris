import xml.etree.ElementTree as ET

from JackGrammar import *
from JackTokenizer import JackTokenizer


class CompilationEngine:

    def __init__(self, tokenizer: JackTokenizer, output_file):
        self._tokenizer = tokenizer
        self._output_file = output_file
        self._compile_class()
        self._write_to_file()

    def _compile_class(self):
        self._current_xml_element = ET.Element('class')

        self._add_token_to_tree(True)  # class

        self._add_token_to_tree(True)  # className

        self._add_token_to_tree(True)  # left curly parenthesis

        self._advance_tokenizer()
        while is_class_var_type(self._tokenizer.get_token()):
            self._compile_class_variable_declaration()  # classVarDec

            self._advance_tokenizer()

        while not is_right_curly_parenthesis(self._tokenizer.get_token()):
            self._compile_subroutine()  # subroutine

            self._advance_tokenizer()

        self._add_token_to_tree(False)  # right curly parenthesis

    def _compile_class_variable_declaration(self):
        previous_xml_element = self._current_xml_element
        self._set_current_xml_element('classVarDec')

        self._add_token_to_tree(False) # static or field

        self._add_token_to_tree(True) # type

        self._add_token_to_tree(True) # varName

        self._advance_tokenizer()
        while is_comma(self._tokenizer.get_token()):
            self._add_token_to_tree(False)  # comma

            self._add_token_to_tree(True) # varName

            self._advance_tokenizer()

        self._add_token_to_tree(False) #semiclon

        self._current_xml_element = previous_xml_element

    def _compile_subroutine(self):
        previous_xml_element = self._current_xml_element
        self._set_current_xml_element('subroutineDec')

        self._add_token_to_tree(False) # constructor or function or method

        self._add_token_to_tree(True) # void or type

        self._add_token_to_tree(True) # subroutineName
    
        self._add_token_to_tree(True) # left parenthesis

        self._advance_tokenizer()
        self._compile_parameter_list()

        self._add_token_to_tree(False) # right parenthesis

        # subroutine body
        self._set_current_xml_element('subroutineBody')
        self._add_token_to_tree(True) # left curly parenthesis

        self._advance_tokenizer()

        while is_var_dec(self._tokenizer.get_token()):
            self._compile_variable_declaration() #varDec
            self._advance_tokenizer()

        self._compile_statements() # statements

        self._add_token_to_tree(False) # right curly parenthesis

        self._current_xml_element = previous_xml_element

    def _compile_parameter_list(self):
        previous_xml_element = self._current_xml_element
        self._set_current_xml_element('parameterList')

        if not is_right_parenthesis(self._tokenizer.get_token()):
            self._add_token_to_tree(False) #type
            self._add_token_to_tree(True) #varName

            self._advance_tokenizer()
            while not is_right_parenthesis(self._tokenizer.get_token()):
                self._add_token_to_tree(False)  # comma
                self._add_token_to_tree(True)  # type
                self._add_token_to_tree(True)  # varName
                self._advance_tokenizer()

        self._current_xml_element = previous_xml_element

    def _compile_variable_declaration(self):
        previous_xml_element = self._current_xml_element
        self._set_current_xml_element('varDec')

        self._add_token_to_tree(False) # var

        self._add_token_to_tree(True) # type

        self._add_token_to_tree(True) # varName

        self._advance_tokenizer()
        while is_comma(self._tokenizer.get_token()):
            self._add_token_to_tree(False)  # comma

            self._add_token_to_tree(True) # varName

            self._advance_tokenizer()

        self._add_token_to_tree(False) #semiclon

        self._current_xml_element = previous_xml_element

    def _compile_statements(self):
        previous_xml_element = self._current_xml_element
        self._set_current_xml_element('statements')

        current_token = self._tokenizer.get_token()
        while(True):
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

        self._current_xml_element = previous_xml_element

    def _compile_do(self):
        previous_xml_element = self._current_xml_element
        self._set_current_xml_element('doStatement')

        self._add_token_to_tree(False) # do

        #subroutine call
        self._add_token_to_tree(True)  # className or varName or subroutineName
        self._advance_tokenizer()
        if is_dot(self._tokenizer.get_token()):
            self._add_token_to_tree(False)  # dot
            self._add_token_to_tree(True)  # subroutine name
            self._advance_tokenizer()
        self._compile_expression_list_with_surrounding_parenthesiss()  # (expression list) # subroutine call

        self._add_token_to_tree(True)  # semicolon

        self._advance_tokenizer()

        self._current_xml_element = previous_xml_element

    def _compile_let(self):
        previous_xml_element = self._current_xml_element
        self._set_current_xml_element('letStatement')

        self._add_token_to_tree(False) # let

        self._add_token_to_tree(True)  # varName

        self._advance_tokenizer()
        if is_left_square_parenthesis(self._tokenizer.get_token()):
            self._add_token_to_tree(False) # left parenthesis

            self._advance_tokenizer()
            self._compile_expression() # expression

            self._add_token_to_tree(False) # right parenthesis

            self._advance_tokenizer()

        self._add_token_to_tree(False)  # equal

        self._advance_tokenizer()
        self._compile_expression() # expression

        self._add_token_to_tree(False) # semicolon

        self._advance_tokenizer()

        self._current_xml_element = previous_xml_element

    def _compile_while(self):
        previous_xml_element = self._current_xml_element
        self._set_current_xml_element('whileStatement')

        self._add_token_to_tree(False) # while

        self._compile_expression_with_surrounding_parenthesiss() # (expression)

        self._compile_statements_with_surrounding_parenthesiss()

        self._advance_tokenizer()

        self._current_xml_element = previous_xml_element

    def _compile_return(self):
        previous_xml_element = self._current_xml_element
        self._set_current_xml_element('returnStatement')

        self._add_token_to_tree(False)  # return

        self._advance_tokenizer()
        if not is_semicolon(self._tokenizer.get_token()):
            self._compile_expression()

        self._add_token_to_tree(False)  # semicolon
        self._advance_tokenizer()

        self._current_xml_element = previous_xml_element

    def _compile_if(self):
        previous_xml_element = self._current_xml_element
        self._set_current_xml_element('ifStatement')

        self._add_token_to_tree(False) # if

        self._compile_expression_with_surrounding_parenthesiss() # (expression)

        self._compile_statements_with_surrounding_parenthesiss() # {statements}

        self._advance_tokenizer()
        if is_else(self._tokenizer.get_token()):
            self._add_token_to_tree(False) # else

            self._compile_statements_with_surrounding_parenthesiss() # {statements}

            self._advance_tokenizer()

        self._current_xml_element = previous_xml_element

    def _compile_expression(self):
        previous_xml_element = self._current_xml_element
        self._set_current_xml_element('expression')

        self._compile_term()
        while is_operation(self._tokenizer.get_token()):
            self._add_token_to_tree(False) # operation
            self._advance_tokenizer()
            self._compile_term()

        self._current_xml_element = previous_xml_element

    def _compile_term(self):
        previous_xml_element = self._current_xml_element
        self._set_current_xml_element('term')

        if is_left_parenthesis(self._tokenizer.get_token()):
            self._add_token_to_tree(False) # left parenthesis
            self._advance_tokenizer()
            self._compile_expression() # expression
            self._add_token_to_tree(False) # right parenthesis
            self._advance_tokenizer()
        elif is_unary_operation(self._tokenizer.get_token()):
            self._add_token_to_tree(False)
            self._advance_tokenizer()
            self._compile_term()
        else:
            self._add_token_to_tree(False)
            self._advance_tokenizer()
            if is_left_square_parenthesis(self._tokenizer.get_token()):
                self._compile_expression_with_surrounding_square_parenthesiss() # [expression]
                self._advance_tokenizer()
            elif is_left_parenthesis(self._tokenizer.get_token()):
                self._compile_expression_list_with_surrounding_parenthesiss()  # (expression list)
                self._advance_tokenizer()
            elif is_dot(self._tokenizer.get_token()):
                self._add_token_to_tree(False)  # dot
                self._add_token_to_tree(True)  # subroutine name
                self._advance_tokenizer()
                self._compile_expression_list_with_surrounding_parenthesiss()  # (expression list)
                self._advance_tokenizer()

        self._current_xml_element = previous_xml_element

    def _compile_expression_list(self):
        previous_xml_element = self._current_xml_element
        self._set_current_xml_element('expressionList')
        if not is_right_parenthesis(self._tokenizer.get_token()):
            self._compile_expression() # expression
            while is_comma(self._tokenizer.get_token()):
                self._add_token_to_tree(False) # comma
                self._advance_tokenizer()
                self._compile_expression() # expression

        self._current_xml_element = previous_xml_element

    def _compile_statements_with_surrounding_parenthesiss(self):
        self._add_token_to_tree(True)  # left curly parenthesis

        self._advance_tokenizer()
        self._compile_statements()  # statements

        self._add_token_to_tree(False)  # right curly parenthesis

    def _compile_expression_with_surrounding_square_parenthesiss(self):
        self._add_token_to_tree(False)  # left square parenthesis

        self._advance_tokenizer()
        self._compile_expression()  # expression

        self._add_token_to_tree(False)  # right square parenthesis

    def _compile_expression_with_surrounding_parenthesiss(self):
        self._add_token_to_tree(True)  # left parenthesis

        self._advance_tokenizer()
        self._compile_expression()  # expression

        self._add_token_to_tree(False)  # right parenthesis

    def _compile_expression_list_with_surrounding_parenthesiss(self):
        self._add_token_to_tree(False) # left parenthesis

        self._advance_tokenizer()
        self._compile_expression_list() # expression list

        self._add_token_to_tree(False) # right parenthesis


    def _advance_tokenizer(self):
        if self._tokenizer.has_more_tokens():
            self._tokenizer.advance()
            return True
        else:
            return False

    def _write_to_file(self):
        self._indent_xml(self._current_xml_element)
        self._output_file.write(ET.tostring(self._current_xml_element, short_empty_elements=False))
        
    def _add_token_to_tree(self, advance=False):
        if advance:
            self._advance_tokenizer()
        self._add_subelement(self._tokenizer.get_token())

    def _set_current_xml_element(self, element):
        self._current_xml_element = ET.SubElement(self._current_xml_element, element)

    def _add_subelement(self, token):
        element = ET.SubElement(self._current_xml_element, get_str_from_type(self._tokenizer.token_type()))
        element.text = ' ' + token + ' '

    def _indent_xml(self, elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self._indent_xml(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
            if not elem.text or not elem.text.strip():
                elem.text = i
