# Decorators that take arguments (decorator factories)
# When you write @decorator(args), Python evaluates decorator(args) first,
# which must return the actual decorator — hence "decorator factory".

import functools
import time


# --------------------------------------------------------------------------
# Recap: plain decorator (no arguments)
# --------------------------------------------------------------------------
# @decorator
# def fn(): ...
#
# is:  fn = decorator(fn)
# decorator receives fn directly.


# --------------------------------------------------------------------------
# Decorator factory (with arguments)
# --------------------------------------------------------------------------
# @decorator_factory(arg)
# def fn(): ...
#
# is:  fn = decorator_factory(arg)(fn)
# decorator_factory(arg) is called first and must RETURN a decorator.
# That returned decorator is then called with fn.
# Result: three levels of nesting — factory → decorator → wrapper.


def repeat(times):
    """Decorator factory: repeat the decorated function `times` times."""

    def decorator(fn):  # the actual decorator
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):  # the replacement function
            for _ in range(times):
                result = fn(*args, **kwargs)
            return result  # return result of last call

        return wrapper

    return decorator  # factory returns the decorator


@repeat(3)
def say(message):
    print(message)


say("hello")
# hello
# hello
# hello


# --------------------------------------------------------------------------
# Another example: prefix — adds a string prefix to the return value
# --------------------------------------------------------------------------


def prefix(text):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return f"{text}{fn(*args, **kwargs)}"

        return wrapper

    return decorator


@prefix(">>> ")
def shout(word):
    return word.upper()


print(shout("python"))  # >>> PYTHON


# --------------------------------------------------------------------------
# Optional arguments: supporting both @decorator and @decorator()
# --------------------------------------------------------------------------
# A common pattern: allow the decorator to be used with or without parentheses.


def repeat2(fn=None, *, times=1):
    """Works as @repeat2 or @repeat2(times=3)."""
    if fn is None:
        # Called as @repeat2(times=3) — return the actual decorator
        return functools.partial(repeat2, times=times)

    # Called as @repeat2 — fn is the decorated function
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        for _ in range(times):
            result = fn(*args, **kwargs)
        return result

    return wrapper


@repeat2  # no parentheses — works fine
def ping():
    print("ping")


@repeat2(times=2)  # with argument — also works
def pong():
    print("pong")


ping()  # ping
pong()  # pong  pong


# --------------------------------------------------------------------------
# Worked example: @slow_down(seconds=0.5)
# --------------------------------------------------------------------------


def slow_down(seconds=1.0):
    """Pause before calling the function."""

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            time.sleep(seconds)
            return fn(*args, **kwargs)

        return wrapper

    return decorator


@slow_down(seconds=0.1)  # small delay so the demo runs quickly
def fetch(url):
    return f"content from {url}"


print(fetch("example.com"))


# --------------------------------------------------------------------------
# Key points
# --------------------------------------------------------------------------
# 1. @decorator(args)  ≡  fn = decorator(args)(fn)
#    Three levels: factory(args) → decorator(fn) → wrapper(*args, **kwargs)
# 2. The factory captures its arguments as closure variables available inside
#    the wrapper.
# 3. Always apply @functools.wraps at the innermost wrapper level.
# 4. For optional arguments, use a keyword-only sentinel (fn=None) pattern.
