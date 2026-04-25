# What is a decorator?
# A decorator is syntactic sugar for wrapping one function with another.
# The core idea: take a function, wrap it in another function, replace the original.

# --------------------------------------------------------------------------
# Step 1: wrapping by hand (no decorator syntax)
# --------------------------------------------------------------------------


def shout_result(fn):
    """A wrapper: calls fn, then shouts the result."""

    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        return str(result).upper()

    return wrapper


def greet(name):
    return f"hello, {name}"


# Manually wrap greet:
greet = shout_result(greet)
print(greet("eusha"))  # HELLO, EUSHA

# This is exactly what @decorator syntax does — it's just cleaner to read.


# --------------------------------------------------------------------------
# Step 2: the @ syntax is 100% equivalent
# --------------------------------------------------------------------------


def bold(fn):
    def wrapper(*args, **kwargs):
        return f"**{fn(*args, **kwargs)}**"

    return wrapper


@bold  # <-- Python executes: greet2 = bold(greet2)
def greet2(name):
    return f"hello, {name}"


print(greet2("eusha"))  # **hello, eusha**


# --------------------------------------------------------------------------
# Step 3: verify they are truly the same thing
# --------------------------------------------------------------------------


def italics(fn):
    def wrapper(*args, **kwargs):
        return f"_{fn(*args, **kwargs)}_"

    return wrapper


def greet3(name):
    return f"hello, {name}"


# These two are identical:
greet3_v1 = italics(greet3)  # manual
greet3_v2 = italics(lambda n: f"hello, {n}")  # also manual, inline


@italics
def greet3_v3(name):
    return f"hello, {name}"


print(greet3_v1("eusha"))  # _hello, eusha_
print(greet3_v3("eusha"))  # _hello, eusha_  — same output


# --------------------------------------------------------------------------
# Key takeaway
# --------------------------------------------------------------------------
# @decorator
# def fn(...):
#     ...
#
# is exactly:
#
# def fn(...):
#     ...
# fn = decorator(fn)
#
# Nothing more, nothing less. The decorator receives the original function
# and must return something callable (usually a wrapper function).
