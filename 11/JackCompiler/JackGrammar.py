from enum import Enum

class TokenType(Enum):
    KEYWORD = 1
    SYMBOL = 2
    INTEGER_CONSTANT = 3
    STRING_CONSTANT = 4
    IDENTIFIER = 5


class IdentifierType(Enum):
    STATIC = 1
    FIELD = 2
    ARG = 3
    LOCAL = 4
    CLASS = 5
    SUBROUTINE = 6


_while = 'while'
_if = 'if'
_let = 'let'
_do = 'do'
_return = 'return'
_else = 'else'
_static = 'static'
_field = 'field'
_var = 'var'
_true = 'true'
_false = 'false'
_null = 'null'
_constructor = 'constructor'
_method = 'method'

_left_parenthesis = '('
_right_parenthesis = ')'
_left_curly_parenthesis = '{'
_right_curly_parenthesis = '}'
_left_square_parenthesis = '['
_right_square_parenthesis = ']'
_dot = '.'
_comma = ','
_semicolon = ';'
_tilda = '~'
_minus = '-'

_class_var_types = [_static, _field]

keywords = ['class', _constructor, 'function', _method, _var, 'int', 'char', 'boolean',
            'void', _true, _false, _null, 'this', _let, _do, _if, _else, _while, _return] + _class_var_types

_operation_symbols = ['+', _minus, '*', '/', '&', '|', '<', '>', '=']

_unary_operation_symbols = ['-', '~']

symbols = [_left_curly_parenthesis, _right_curly_parenthesis, _left_parenthesis, _right_parenthesis,
           _left_square_parenthesis, _right_square_parenthesis, _dot, _comma, _semicolon, _tilda] + _operation_symbols

token_type_strings = {TokenType.KEYWORD: 'keyword', TokenType.SYMBOL: 'symbol',
                      TokenType.INTEGER_CONSTANT: 'integerConstant', TokenType.STRING_CONSTANT: 'stringConstant',
                      TokenType.IDENTIFIER: 'identifier'}

identifier_type_strings = {IdentifierType.STATIC: 'static', IdentifierType.FIELD: 'field',
                           IdentifierType.LOCAL: 'local', IdentifierType.ARG: 'argument',
                           IdentifierType.CLASS: 'class', IdentifierType.SUBROUTINE: 'subroutine'}

identifier_type = {'static' : IdentifierType.STATIC, 'field': IdentifierType.FIELD,
                    'local' : IdentifierType.LOCAL, 'argument' : IdentifierType.ARG,
                    'class' : IdentifierType.CLASS, 'subroutine' : IdentifierType.SUBROUTINE}


def get_str_from_token_type(type):
    return token_type_strings[type]


def get_str_from_identifier_type(type):
    return identifier_type_strings[type]


def get_identifier_type_from_str(str):
    return identifier_type[str]


def is_while(str):
    return str == _while


def is_let(str):
    return str == _let


def is_if(str):
    return str == _if


def is_do(str):
    return str == _do


def is_return(str):
    return str == _return


def is_else(str):
    return str == _else


def is_dot(str):
    return str == _dot


def is_comma(str):
    return str == _comma


def is_semicolon(str):
    return str == _semicolon


def is_operation(str):
    return str in _operation_symbols


def is_unary_operation(str):
    return str in _unary_operation_symbols


def is_class_var_type(str):
    return str in _class_var_types


def is_var_dec(str):
    return str == _var


def is_left_parenthesis(str):
    return str == _left_parenthesis


def is_right_parenthesis(str):
    return str == _right_parenthesis


def is_left__curly_parenthesis(str):
    return str == _left_curly_parenthesis


def is_right_curly_parenthesis(str):
    return str == _right_curly_parenthesis


def is_left_square_parenthesis(str):
    return str == _left_square_parenthesis


def is_right_square_parenthesis(str):
    return str == _right_square_parenthesis


def is_true(str):
    return str == _true


def is_false(str):
    return str == _false


def is_null(str):
    return str == _null


def is_constructor(str):
    return str == _constructor


def is_method(str):
    return str == _method
