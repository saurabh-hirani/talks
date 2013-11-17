#!/usr/bin/env python
"""
This program gives a basic example of callbacks

>>> call_func('f1', 1)
'in func1 with arg [1]'

>>> call_func('f2', 2)
'in func2 with arg [2]'
"""

def func1(arg):
    return 'in func1 with arg [%s]' % str(arg) 

def func2(arg):
    return 'in func2 with arg [%s]' % str(arg) 

def get_callbacks_dict():
    return { 'f1': func1, 'f2': func2 }

def call_func(func_name, arg):
    """
    Given a func name - look it up in callbacks dict and call it with arg
    """
    return get_callbacks_dict()[func_name](str(arg))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
