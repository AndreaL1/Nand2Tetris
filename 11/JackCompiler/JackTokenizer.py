import re

from FileHelper import *
from JackGrammar import *


_line_comment_symbol = '//'
_multiline_comment_start_symbol = '/*'
_multiline_comment_end_symbol = '*/'
_doc_comment_start_symbol = '/**'
_doc_comment_end_symbol = '*/'

_symbol_pattern = r'^[' + ''.join(["\\" + symbol for symbol in symbols]) + ']'
_string_constant_pattern = r'^(\")(.*?)(\")'
_integer_constant_pattern = r'^[-+]?[0-9]+'
_keyword_pattern = r'' + ''.join(['(^' + keyword + ')' + '|' for keyword in keywords[0:-1]]) + '(^' + keywords[-1] + ')'
_identifier_pattern = r'^([a-zA-Z_])([a-zA-Z0-9_]*)'

class JackTokenizer:
    def __init__(self, input_file):
        self._content = _get_content(input_file)
        self._index = 0
        self._current_token = None
        self._set_scanners()

    def has_more_tokens(self):
        return self._index < len(self._content)

    def advance(self):
        next_symbol_constant_token = self._next_symbol_token()
        if next_symbol_constant_token is not None:
            self._current_token_type = TokenType.SYMBOL
            self._set_current_token(next_symbol_constant_token)
        else:
            next_string_constant_token = self._next_string_constant_token()
            if next_string_constant_token is not None:
                self._current_token_type = TokenType.STRING_CONSTANT
                self._set_current_token(next_string_constant_token)
            else:
                next_integer_constant_token = self._next_integer_constant_token()
                if next_integer_constant_token is not None:
                    self._current_token_type = TokenType.INTEGER_CONSTANT
                    self._set_current_token(next_integer_constant_token)
                else:
                    next_keyword_token = self._next_keyword_token()
                    next_identifier_token = self._next_identifier_token()
                    if _set_keyword_token(next_keyword_token, next_identifier_token):
                        self._current_token_type = TokenType.KEYWORD
                        self._set_current_token(next_keyword_token)
                    elif next_identifier_token is not None:
                            self._current_token_type = TokenType.IDENTIFIER
                            self._set_current_token(next_identifier_token)
        self._increase_index()

    def token_type(self):
        return self._current_token_type

    def get_token(self):
        return self._current_token

    def _next_symbol_token(self):
        return self._symbol_scanner.search(self._content[self._index])

    def _next_string_constant_token(self):
        return self._string_constant_scanner.search(self._content[self._index:])

    def _next_integer_constant_token(self):
        return self._integer_constant_scanner.search(self._content[self._index:])

    def _next_keyword_token(self):
        return self._keyword_scanner.search(self._content[self._index:])

    def _next_identifier_token(self):
        return self._identifier_scanner.search(self._content[self._index:])

    def _set_current_token(self, token_match):
        start_index = self._get_token_start_index()
        end_index = self._get_token_end_index(token_match.end())
        self._current_token = self._content[start_index:end_index]

    def _increase_index(self):
        self._index += len(self._current_token)
        if self.token_type() == TokenType.STRING_CONSTANT:
            self._index += 2
        while(self._current_content_is_space()):
            self._index +=1

    def _current_content_is_space(self):
        if not self.has_more_tokens():
            return False
        return self._content[self._index] == ' '

    def _set_scanners(self):
        self._symbol_scanner = re.compile(_symbol_pattern)
        self._string_constant_scanner = re.compile(_string_constant_pattern)
        self._integer_constant_scanner = re.compile(_integer_constant_pattern)
        self._keyword_scanner = re.compile(_keyword_pattern)
        self._identifier_scanner = re.compile(_identifier_pattern)

    def _get_token_start_index(self):
        if self.token_type() == TokenType.STRING_CONSTANT:
            return self._index + 1
        else:
            return self._index

    def _get_token_end_index(self, end_index):
        if self.token_type() == TokenType.STRING_CONSTANT:
            return self._index + end_index - 1
        else:
            return self._index + end_index


def _get_content(file):
    content = read_file(file)
    return _get_raw_commands(content)


def _get_raw_commands(content):
    return _concatenate_to_string(_remove_comments(_remove_empty_lines(_strip_content(content))))


def _remove_line_comment(content, symbol):
    return [line[:line.find(symbol)] if _line_comment_symbol in line else line for line in content]


def _remove_multiline_comment(content, comment_start_symbol, comment_end_symbol):
    result_content = []
    inside_comment = False
    for line in content:
        if not inside_comment:
            if comment_start_symbol not in line:
                result_content.append(line)
            else:
                result_content.append(line[:line.find(comment_start_symbol)])
                if comment_end_symbol in line:
                    result_content.append(get_content_from_line_with_multiline_comment_end_symbol(line, comment_end_symbol))
                else:
                    inside_comment = True
        else:
            if comment_end_symbol in line:
                result_content.append(get_content_from_line_with_multiline_comment_end_symbol(line, comment_end_symbol))
                inside_comment = False
    return result_content


def get_content_from_line_with_multiline_comment_end_symbol(line, comment_end_symbol):
    return line[line.find(comment_end_symbol)+ len(comment_end_symbol):]


def _remove_comments(content):
    return _remove_multiline_comment(
        _remove_multiline_comment(
            _remove_line_comment(content, _line_comment_symbol),
            _multiline_comment_start_symbol, _multiline_comment_end_symbol),
        _doc_comment_start_symbol, _doc_comment_end_symbol)


def _strip_content(content):
    return [x.strip() for x in content]


def _remove_empty_lines(content):
    return [line for line in content if len(line) > 0]


def _concatenate_to_string(content):
    return ''.join(content)


def _set_keyword_token(keyword_token, identifier_token):
    if keyword_token is None:
        return False
    if identifier_token is None:
        return True
    if keyword_token.end() >= identifier_token.end():
        return True
    return False
