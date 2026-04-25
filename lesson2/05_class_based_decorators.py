# Class-based decorators using __call__
# Any object with a __call__ method is callable and can be used as a decorator.
# Classes are useful when the decorator needs to maintain state between calls.

import functools


# --------------------------------------------------------------------------
# The simplest class-based decorator
# --------------------------------------------------------------------------
# @Decorator applied to fn causes Python to call: fn = Decorator(fn)
# So __init__ receives the function, and __call__ is invoked on each call.


class Shout:
    """Uppercases the return value of the decorated function."""

    def __init__(self, fn):
        functools.update_wrapper(
            self, fn
        )  # equivalent of @functools.wraps for classes
        self.fn = fn

    def __call__(self, *args, **kwargs):
        result = self.fn(*args, **kwargs)
        return str(result).upper()


@Shout
def greet(name):
    """Return a greeting."""
    return f"hello, {name}"


print(greet("eusha"))  # HELLO, EUSHA
print(greet.__name__)  # greet  ✓ (thanks to update_wrapper)
print(greet.__doc__)  # Return a greeting.  ✓


# --------------------------------------------------------------------------
# Stateful decorator: counting calls
# --------------------------------------------------------------------------
# A class decorator can store state in instance attributes — something a
# closure-based decorator can do but requires more ceremony.


class CountCalls:
    """Tracks how many times the decorated function has been called."""

    def __init__(self, fn):
        functools.update_wrapper(self, fn)
        self.fn = fn
        self.call_count = 0  # state lives on the instance

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        print(f"[call #{self.call_count}] {self.fn.__name__}")
        return self.fn(*args, **kwargs)


@CountCalls
def compute(x):
    return x * 2


compute(1)  # [call #1] compute
compute(2)  # [call #2] compute
compute(3)  # [call #3] compute

print(compute.call_count)  # 3  — accessible directly on the decorated function


# --------------------------------------------------------------------------
# Class-based decorator factory (decorator with arguments)
# --------------------------------------------------------------------------
# When the decorator takes arguments, __init__ receives those arguments
# and __call__ receives the function.  A second __call__ (or a nested
# function) then acts as the actual wrapper.


class Repeat:
    """Repeat the function call n times."""

    def __init__(self, times=2):
        self.times = times

    def __call__(self, fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for _ in range(self.times):
                result = fn(*args, **kwargs)
            return result

        return wrapper


@Repeat(times=3)
def say(msg):
    print(msg)


say("hello")
# hello
# hello
# hello


# --------------------------------------------------------------------------
# Stateful rate limiter — a realistic use of class state
# --------------------------------------------------------------------------
import time


class RateLimit:
    """Allow at most `calls` calls per `period` seconds."""

    def __init__(self, calls=5, period=1.0):
        self.calls = calls
        self.period = period
        self.timestamps: list[float] = []

    def __call__(self, fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            now = time.monotonic()
            # Drop timestamps outside the current window
            self.timestamps = [
                t for t in self.timestamps if now - t < self.period
            ]
            if len(self.timestamps) >= self.calls:
                raise RuntimeError(
                    f"{fn.__name__} exceeded {self.calls} calls/{self.period}s"
                )
            self.timestamps.append(now)
            return fn(*args, **kwargs)

        return wrapper


@RateLimit(calls=3, period=5.0)
def api_call(endpoint):
    return f"response from {endpoint}"


print(api_call("/users"))  # response from /users
print(api_call("/posts"))  # response from /posts
print(api_call("/items"))  # response from /items
try:
    print(api_call("/extra"))  # RuntimeError: exceeded 3 calls
except RuntimeError as e:
    print(e)


# --------------------------------------------------------------------------
# When to choose a class over a closure
# --------------------------------------------------------------------------
# Use a CLASS decorator when:
#   - you need persistent state across calls (counters, caches, timestamps)
#   - you want to expose that state as public attributes (e.g. .call_count)
#   - the logic is complex enough that splitting across methods improves clarity
#
# Use a CLOSURE decorator when:
#   - the decorator is stateless or has only simple state
#   - you prefer a lighter, more functional style
