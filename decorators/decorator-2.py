#!/usr/bin/env python

def decorator(func):
    def wrapper_around_func():
        print "Decorator calling func"
        func()
        print "Decorator called func"
    return wrapper_around_func
 
# func = decorator(func)
@decorator
def func():
    print "In the function"
 
func()
print func.__name__
