def f1(): pass

class A():
    def m1(): pass

x = f1
y = f1
z = f1
print "\n==== id for function f1 ===="
print 'id(f1) = ' + str(id(f1))
print 'id(x) = ' + str(id(x))
print 'id(y) = ' + str(id(y))
print 'id(z) = ' + str(id(z))

x = A
y = A
z = A
print "\n==== id for class A ===="
print 'id(A) = ' + str(id(A))
print 'id(x) = ' + str(id(x))
print 'id(y) = ' + str(id(y))
print 'id(z) = ' + str(id(z))

x = A.m1
y = A.m1
z = A.m1
print "\n==== id for method A.m1 ===="
print 'id(A.m1) = ' + str(id(A.m1))
print 'id(x) = ' + str(id(x))
print 'id(y) = ' + str(id(y))
print 'id(z) = ' + str(id(z))

print 'x is y ' + str(x is y)
print 'x == y ' + str(x == y)
