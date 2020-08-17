def announce(f):
    def wrapper():
        print("About to run the function...")
        f()
        print("Here are the results")
    return wrapper


@announce
def hello():
    print('Hello, world!')


hello()
