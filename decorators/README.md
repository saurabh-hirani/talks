# Using decorators to register Callbacks

- Detailed blog post - [Using decorators to register callbacks](http://curiosityhealsthecat.blogspot.in/2013/07/using-python-decorators-for-registering_8614.html)

## Callbacks - overview

- A registered function which is called when an event occurs

- e.g. When url contains '/main_page' call the main page function

### callback-1.py

- Sample callback which maps function name description with the function

- When dictionary is looked up for that function name - it returns the function
  reference

### callback-2.py

- Registering callbacks via a class

- Similar to callback-1 - but with dictionary registration and look up 
  hidden inside class

## Decorators - overview

### decorator-1.py

- A wrapper around a function to add pre/post functionality to the function

- Takes function reference as an argument and returns a wrapper which
  when called would do some pre/post work and call the target function
  in between

### decorator-2.py

- Using the pythonic way 

- equivalent to decorator-1.py in functionality

### decorator-3.py

- Using functools.wraps

- Preserves the function name and other function attributes like function doc

- standard way

### decorator-4.py

- Decorator with arguments

## Marrying callbacks and decorator

### callback-decorator.py

- Register callbacks using decorators 

### decorator-5.py

- Sample example of using nested decorators
