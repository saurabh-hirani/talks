#!/usr/bin/env python
 
def decorator(func):
    def wrapper_around_func():
        print "Decorator calling func"
        func()
        print "Decorator called func"
    return wrapper_around_func
 
def func():
    print "In the function"

func = decorator(func)
func()
