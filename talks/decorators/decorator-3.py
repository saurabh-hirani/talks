#!/usr/bin/env python

from functools import wraps
 
def decorator(func):
    @wraps(func)
    def wrapper_around_func():
        print "Decorator calling func" 
        func()
        print "Decorator called func"
    return wrapper_around_func
 
@decorator
def func():
    print "In the function"
 
func()
print func.__name__
