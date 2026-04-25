# Functions as objects
# In Python, functions are first-class objects: they can be assigned to variables,
# stored in data structures, passed as arguments, and returned from other functions.


def greet(name):
    return f"Hello, {name}!"


# Assign a function to a variable
say_hello = greet
print(say_hello("Eusha"))  # Hello, Eusha!

# Functions have attributes just like other objects
print(greet.__name__)  # greet
print(type(greet))  # <class 'function'>


# Store functions in a list
def shout(text):
    return text.upper()


def whisper(text):
    return text.lower()


formatters = [shout, whisper]
for fn in formatters:
    print(fn("Hello World"))  # HELLO WORLD / hello world


# Pass a function as an argument
def apply(fn, value):
    return fn(value)


print(apply(shout, "quiet"))  # QUIET
print(apply(len, "Python"))  # 6  — built-ins work too


# Return a function from a function
def get_formatter(style):
    if style == "shout":
        return shout
    return whisper


formatter = get_formatter("shout")
print(formatter("hello"))  # HELLO
