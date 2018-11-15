from JackGrammar import *


class SymbolTable:
    def __init__(self):
        self._class_table = {}
        self._current_var_idx = {IdentifierType.FIELD: -1, IdentifierType.STATIC : -1,
                                 IdentifierType.ARG : -1, IdentifierType.LOCAL: -1}

    def start_subroutine(self):
        self._subroutine_table = {}
        self._current_var_idx[IdentifierType.ARG] = -1
        self._current_var_idx[IdentifierType.LOCAL] = -1

    def define(self, name, type, kind):
        self._current_var_idx[kind] += 1
        if (kind == IdentifierType.STATIC) | (kind == IdentifierType.FIELD):
            self._class_table[name] = {'type' : type, 'kind' : kind, 'idx' : self._current_var_idx[kind]}
        elif (kind == IdentifierType.ARG) | (kind == IdentifierType.LOCAL):
            self._subroutine_table[name] = {'type' : type, 'kind' : kind, 'idx' : self._current_var_idx[kind]}

    def var_count(self, kind):
        return self._current_var_idx[kind] + 1

    def kind_of(self, name):
        if name in self._class_table:
            return self._class_table[name]['kind']
        return self._subroutine_table[name]['kind']

    def type_of(self, name):
        if name in self._class_table:
            return self._class_table[name]['type']
        return self._subroutine_table[name]['type']

    def index_of(self, name):
        if name in self._class_table:
            return self._class_table[name]['idx']
        return self._subroutine_table[name]['idx']

    def is_var(self, name):
        if (name in self._subroutine_table) | (name in self._class_table):
            return True
        return False
