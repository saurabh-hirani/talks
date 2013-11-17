#!/usr/bin/env python
 
class MyApp():
    def __init__(self):
        self.func_map = {}
 
    def register(self, name):
        def func_wrapper(func):
            self.func_map[name] = func
            return func
        return func_wrapper
 
    def call_registered(self, name=None):
        func = self.func_map.get(name, None)
        if func is None:
            raise Exception("No function registered against - " + str(name))
        return func()
 
app = MyApp()
 
@app.register('/')
def main_page_func():
    return "This is the main page."
 
@app.register('/next_page')
def next_page_func():
    return "This is the next page."

# @app.register('/') over main_page_func
# leads to
# - main_page_func = @app.register('/')(main_page_func)
#   - @app.register('/') return func_wrapper with name set to '/'
#   - main_page_func = func_wrapper(main_page_func)
#   - func wrapper registers '/' against main_page_func and returns 
#     main_page_func as is
print app.call_registered('/')
print app.call_registered('/next_page')
