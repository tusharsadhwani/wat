from ctypes import pythonapi, py_object
import sys

def swap(value_a, value_b):
    parent_frame = sys._getframe(1)
    parent_locals = parent_frame.f_locals

    bytecode = parent_frame.f_code.co_code
    index = parent_frame.f_lasti

    LOAD_NAME = 101
    LOAD_FAST = 124
    # Ensure last two calls were load_name's
    opcode_a, index_a, opcode_b, index_b = bytecode[index-4:index]
    if (
        opcode_a not in (LOAD_NAME, LOAD_FAST)
        or opcode_b not in (LOAD_NAME, LOAD_FAST)
    ):
        raise ValueError("Can only call swap on variables")

    # Get the variables from the last two instruction values

    parent_names = parent_frame.f_code.co_names
    parent_varnames = parent_frame.f_code.co_varnames
    if opcode_a == LOAD_NAME:
        var_a = parent_names[index_a]
    else:
        var_a = parent_varnames[index_a]

    if opcode_b == LOAD_NAME:
        var_b = parent_names[index_b]
    else:
        var_b = parent_varnames[index_b]

    # Swap with received values
    parent_locals[var_a], parent_locals[var_b] = value_b, value_a

    # Write changes to frame's fastlocals so it persists
    pythonapi.PyFrame_LocalsToFast.argtypes = [py_object]
    pythonapi.PyFrame_LocalsToFast(parent_frame)


def main():
    x = 3
    y = 5
    print(f'{x=}, {y=}')

    swap(x, y)
    print(f'{x=}, {y=}')
