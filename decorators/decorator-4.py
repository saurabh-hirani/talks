def log_deco(loglevel):
    def deco1(func):
        def deco_wrapper():
            print "------"
            if loglevel == 'info':
                print "info log"
            else:
                print "debug log " + func.__name__ 
            func()
            print "------"
        return deco_wrapper
    return deco1

@log_deco('info')
def func1():
    print "here"

@log_deco('debug')
def func2():
    print "there"

def func3():
    print 'everywhere'

# @log_deco('info') over func1 leads to
# - func1 = @log_deco('info')(func1)
#   - @log_deco('info') returns deco_wrapper with loglevel set to '/'
#   - func1 = deco_wrapper(func1)
#   - deco wrapper 

func1()
func2()
log_deco('debug')(func3)()
