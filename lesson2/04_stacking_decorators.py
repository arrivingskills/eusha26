# Stacking multiple decorators (execution order)
# When you stack decorators, they are applied bottom-up at definition time,
# but the wrappers execute top-down at call time.

import functools


# --------------------------------------------------------------------------
# Setup: two simple decorators that announce themselves
# --------------------------------------------------------------------------


def decorator_A(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print("A: before")
        result = fn(*args, **kwargs)
        print("A: after")
        return result

    return wrapper


def decorator_B(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print("B: before")
        result = fn(*args, **kwargs)
        print("B: after")
        return result

    return wrapper


def decorator_C(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print("C: before")
        result = fn(*args, **kwargs)
        print("C: after")
        return result

    return wrapper


# --------------------------------------------------------------------------
# Application order at DEFINITION time: bottom-up
# --------------------------------------------------------------------------
# @A
# @B
# @C
# def fn(): ...
#
# Python reads bottom to top and applies each decorator:
#   step 1: fn = C(fn)      — C wraps the original fn
#   step 2: fn = B(fn)      — B wraps C's wrapper
#   step 3: fn = A(fn)      — A wraps B's wrapper
#
# Think of it as layers of an onion: A is outermost, C is innermost.


@decorator_A
@decorator_B
@decorator_C
def hello():
    print("hello!")


hello()
# Output:
# A: before
# B: before
# C: before
# hello!
# C: after
# B: after
# A: after


# --------------------------------------------------------------------------
# Execution order at CALL time: top-down (outermost first)
# --------------------------------------------------------------------------
# Calling hello() runs A's wrapper first, which calls B's wrapper,
# which calls C's wrapper, which calls the original function.
# The "after" steps unwind in reverse: C → B → A.


# --------------------------------------------------------------------------
# Manual equivalence — stacking is just repeated assignment
# --------------------------------------------------------------------------


def greet(name):
    print(f"greet: {name}")


# @A @B @C greet  is literally:
greet_stacked = decorator_A(decorator_B(decorator_C(greet)))
greet_stacked("eusha")
# A: before  B: before  C: before  greet: eusha  C: after  B: after  A: after


# --------------------------------------------------------------------------
# Practical example: @bold and @italics (order matters!)
# --------------------------------------------------------------------------


def bold(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return f"<b>{fn(*args, **kwargs)}</b>"

    return wrapper


def italics(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return f"<i>{fn(*args, **kwargs)}</i>"

    return wrapper


@bold  # outermost
@italics  # innermost (applied first)
def text1():
    return "python"


@italics  # outermost
@bold  # innermost (applied first)
def text2():
    return "python"


print(text1())  # <b><i>python</i></b>  — bold wraps italics
print(text2())  # <i><b>python</b></i>  — italics wraps bold


# --------------------------------------------------------------------------
# Key rule of thumb
# --------------------------------------------------------------------------
# Reading the stack top-to-bottom tells you the execution order of "before" code:
#
# @log_call        ← runs first (outermost)
# @check_auth      ← runs second
# @validate_input  ← runs last (innermost, closest to the real function)
# def endpoint(): ...
#
# Order often matters for correctness: you usually want auth checked
# before expensive validation, for example.
