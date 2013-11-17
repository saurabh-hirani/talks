
def decorator_2(func):
    def wrapper2(*args):
        print "deco 2"
        func(*args)
        print "deco 2"
    return wrapper2

def decorator_1(func):
    def wrapper1(*args):
        print "deco 1"
        func(*args)
        print "deco 1"
    return wrapper1

@decorator_2
@decorator_1
def func1(arg1):
  print "inner - " + arg1

# func1 = decorator_2(decorator_1(func1))
func1('this')
