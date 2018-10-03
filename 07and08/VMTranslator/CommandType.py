from enum import Enum

_push_string = 'push'
_pop_string = 'pop'
_add_string = 'add'
_sub_string = 'sub'
_neg_string = 'neg'
_eq_string = 'eq'
_gt_string = 'gt'
_lt_string = 'lt'
_and_string = 'and'
_or_string = 'or'
_not_string = 'not'
_label_string = 'label'
_goto_string = 'goto'
_if_goto_string = 'if-goto'
_function_string = 'function'
_return_string = 'return'
_call_string = 'call'


class CommandType(Enum):
    C_ARITHMETIC = 1
    C_PUSH = 2
    C_POP = 3
    C_LABEL = 4
    C_GOTO = 5
    C_IF_GOTO = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9

    @classmethod
    def get_type_from_string(cls, string):
        if _arithmetic_command(string):
            return cls.C_ARITHMETIC
        if _push_command( string):
            return cls.C_PUSH
        if _pop_command(string):
            return cls.C_POP
        if _label_command(string):
            return cls.C_LABEL
        if _goto_command(string):
            return cls.C_GOTO
        if _if_goto_command(string):
            return cls.C_IF_GOTO
        if _function_command(string):
            return cls.C_FUNCTION
        if _return_command(string):
            return cls.C_RETURN
        if _call_command(string):
            return cls.C_CALL
        return None


def _arithmetic_command(string):
    return string == _add_string or \
           string == _sub_string or \
           string == _neg_string or \
           string == _eq_string or \
           string == _gt_string or \
           string == _lt_string or \
           string == _and_string or \
           string == _or_string or \
           string == _not_string


def _push_command(string):
    return string == _push_string


def _pop_command(string):
    return string == _pop_string


def _label_command(string):
    return string == _label_string


def _goto_command(string):
    return string == _goto_string


def _if_goto_command(string):
    return string == _if_goto_string


def _function_command(string):
    return string == _function_string


def _return_command(string):
    return string == _return_string


def _call_command(string):
    return string == _call_string
