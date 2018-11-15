from enum import Enum

_add_string = 'add'
_sub_string = 'sub'
_neg_string = 'neg'
_eq_string = 'eq'
_gt_string = 'gt'
_lt_string = 'lt'
_and_string = 'and'
_or_string = 'or'
_not_string = 'not'


class ArithmeticCommandType(Enum):
    ADD = 1
    SUB = 2
    NEG = 3
    EQ = 4
    GT = 5
    LT = 6
    AND= 7
    OR = 8
    NOT = 9

def get_type_from_string(string):
    if _add_op(string):
        return ArithmeticCommandType.ADD
    if _sub_op(string):
        return ArithmeticCommandType.SUB
    if _neg_op(string):
        return ArithmeticCommandType.NEG
    if _eq_op(string):
        return ArithmeticCommandType.EQ
    if _gt_op(string):
        return ArithmeticCommandType.GT
    if _lt_op(string):
        return ArithmeticCommandType.LT
    if _and_op(string):
        return ArithmeticCommandType.AND
    if _or_op(string):
        return ArithmeticCommandType.OR
    if _not_op(string):
        return ArithmeticCommandType.NOT
    return None

def get_string_from_type(string):
    if string == ArithmeticCommandType.ADD:
        return _add_string
    if string == ArithmeticCommandType.SUB:
        return _sub_string
    if string == ArithmeticCommandType.NEG:
        return _neg_string
    if string == ArithmeticCommandType.EQ:
        return _eq_string
    if string == ArithmeticCommandType.GT:
        return _gt_string
    if string == ArithmeticCommandType.LT:
        return _lt_string
    if string == ArithmeticCommandType.AND:
        return _and_string
    if string == ArithmeticCommandType.OR:
        return _or_string
    if string == ArithmeticCommandType.NOT:
        return _not_string
    return None

def _add_op(op_string):
    if op_string == _add_string:
        return ArithmeticCommandType.ADD


def _sub_op(op_string):
    if op_string == _sub_string:
        return ArithmeticCommandType.SUB


def _neg_op(op_string):
    if op_string == _neg_string:
        return ArithmeticCommandType.NEG


def _eq_op(op_string):
    if op_string == _eq_string:
        return ArithmeticCommandType.EQ


def _gt_op(op_string):
    if op_string == _gt_string:
        return ArithmeticCommandType.GT


def _lt_op(op_string):
    if op_string == _lt_string:
        return ArithmeticCommandType.LT


def _and_op(op_string):
    if op_string == _and_string:
        return ArithmeticCommandType.AND


def _or_op(op_string):
    if op_string == _or_string:
        return ArithmeticCommandType.OR


def _not_op(op_string):
    if op_string == _not_string:
        return ArithmeticCommandType.NOT
