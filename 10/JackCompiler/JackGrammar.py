from enum import Enum

class TokenType(Enum):
    KEYWORD = 1
    SYMBOL = 2
    INTEGER_CONSTANT = 3
    STRING_CONSTANT = 4
    IDENTIFIER = 5


_while = 'while'
_if = 'if'
_let = 'let'
_do = 'do'
_return = 'return'
_else = 'else'
_static = 'static'
_field = 'field'
_var = 'var'

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

keywords = ['class', 'constructor', 'function', 'method', _var, 'int', 'char', 'boolean',
            'void', 'true', 'false', 'null', 'this', _let, _do, _if, _else, _while, _return] + _class_var_types

_operation_symbols = ['+', _minus, '*', '/', '&', '|', '<', '>', '=']

_unary_operation_symbols = ['-', '~']

symbols = [_left_curly_parenthesis, _right_curly_parenthesis, _left_parenthesis, _right_parenthesis,
           _left_square_parenthesis, _right_square_parenthesis, _dot, _comma, _semicolon, _tilda] + _operation_symbols

token_type_strings = {TokenType.KEYWORD: 'keyword', TokenType.SYMBOL: 'symbol',
                      TokenType.INTEGER_CONSTANT: 'integerConstant', TokenType.STRING_CONSTANT: 'stringConstant',
                      TokenType.IDENTIFIER: 'identifier'}


def get_str_from_type(type):
    return token_type_strings[type]


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