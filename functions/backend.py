# These are our *backend* methods.
# These methods are for things that are done async from other stuff, as to not
# hang up the client and the application. Our queue will handle
# calling these messages after grabbing them from the db.


def create(a, b, c):
    print("Create Called!")
    print("params: %s - %s - %s" % (a, b, c))
    pass