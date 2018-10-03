from enum import Enum

_local_string = 'local'
_argument_string = 'argument'
_this_string = 'this'
_that_string = 'that'
_constant_string = 'constant'
_static_string = 'static'
_temp_string = 'temp'
_pointer_string = 'pointer'


class MemorySegmentType(Enum):
    LOCAL = 1
    ARGUMENT = 2
    THIS = 3
    THAT = 4
    CONSTANT = 5
    STATIC = 6
    TEMP = 7
    POINTER = 8

    @classmethod    
    def get_type_from_string(cls, string):
        if local_segment(string):
            return cls.LOCAL
        if argument_segment(string):
            return cls.ARGUMENT
        if this_segment(string):
            return cls.THIS
        if that_segment(string):
            return cls.THAT
        if constant_segment(string):
            return cls.CONSTANT
        if static_segment(string):
            return cls.STATIC
        if temp_segment(string):
            return cls.TEMP
        if pointer_segment(string):
            return cls.POINTER
        return None
    

def local_segment(seg_string):
    return seg_string == _local_string


def argument_segment(seg_string):
    return seg_string == _argument_string


def this_segment(seg_string):
    return seg_string == _this_string


def that_segment(seg_string):
    return seg_string == _that_string


def constant_segment(seg_string):
    return seg_string == _constant_string


def static_segment(seg_string):
    return seg_string == _static_string


def temp_segment(seg_string):
    return seg_string == _temp_string


def pointer_segment(seg_string):
    return seg_string == _pointer_string