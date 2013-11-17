#!/usr/bin/env python
 
"""
Register the function via class and call it

>>> app = MyApp()

>>> app.register('/', main_page_func)

>>> app.register('/next_page', main_page_func)

>>> app.call_registered('/')
'This is the main page.'

>>> app.call_registered('/next_page')
'This is the main page.'

>>> app.call_registered('/testpage')
Traceback (most recent call last):
...
ValueError: No function registered against - /testpage
"""
 
class MyApp():
    def __init__(self):
        self.func_map = {}
 
    def register(self, name, func):
        self.func_map[name] = func
 
    def call_registered(self, name=None):
        func = self.func_map.get(name, None)
        if func is None:
            raise ValueError("No function registered against - " + str(name))
        return func()
 
app = MyApp()
 
def main_page_func():
    return "This is the main page."
 
def next_page_func():
    return "This is the next page."

if __name__ == '__main__':
    import doctest
    doctest.testmod()
