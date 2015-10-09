# This is our decorator
def simple_decorator(f):
    # This is the new function we're going to return
    # This function will be used in place of our original definition
    def wrapper():
        print "Entering Function"
        x=f()
        return x

    return wrapper

@simple_decorator 
def hello():
    return "Hello World"

x=hello()
print x