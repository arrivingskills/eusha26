# Writing a basic decorator with functools.wraps
# Without functools.wraps, wrapping a function clobbers its metadata
# (__name__, __doc__, __annotations__, etc.).  Always use it.

import functools


# --------------------------------------------------------------------------
# Problem: naive wrapper loses the function's identity
# --------------------------------------------------------------------------


def naive_decorator(fn):
    def wrapper(*args, **kwargs):
        print(f"calling something...")
        return fn(*args, **kwargs)

    return wrapper


@naive_decorator
def add(a: int, b: int) -> int:
    """Return the sum of a and b."""
    return a + b


print(add.__name__)  # wrapper   ← WRONG, should be 'add'
print(add.__doc__)  # None      ← WRONG, docstring is gone


# --------------------------------------------------------------------------
# Fix: use @functools.wraps to copy the original function's metadata
# --------------------------------------------------------------------------


def better_decorator(fn):
    @functools.wraps(fn)  # <-- copies __name__, __doc__, __wrapped__, etc.
    def wrapper(*args, **kwargs):
        print(f"calling {fn.__name__}...")
        return fn(*args, **kwargs)

    return wrapper


@better_decorator
def multiply(a: int, b: int) -> int:
    """Return the product of a and b."""
    return a * b


print(multiply.__name__)  # multiply  ✓
print(multiply.__doc__)  # Return the product of a and b.  ✓
print(
    multiply.__wrapped__
)  # <function multiply ...>  — the original, unwrapped fn


# --------------------------------------------------------------------------
# A general-purpose template for any decorator
# --------------------------------------------------------------------------


def my_decorator(fn):
    """Decorator template — copy this as a starting point."""

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # --- before ---
        result = fn(*args, **kwargs)
        # --- after ---
        return result

    return wrapper


# --------------------------------------------------------------------------
# Example: a 'verbose' decorator that logs calls and return values
# --------------------------------------------------------------------------


def verbose(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        arg_str = ", ".join(
            [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
        )
        print(f"→ {fn.__name__}({arg_str})")
        result = fn(*args, **kwargs)
        print(f"← {fn.__name__} returned {result!r}")
        return result

    return wrapper


@verbose
def power(base, exponent=2):
    """Raise base to exponent."""
    return base**exponent


power(3)  # → power(3)  ← power returned 9
power(2, 10)  # → power(2, 10)  ← power returned 1024
power(5, exponent=3)  # → power(5, exponent=3)  ← power returned 125


# --------------------------------------------------------------------------
# Key points
# --------------------------------------------------------------------------
# 1. Always use @functools.wraps(fn) inside your decorator — no exceptions.
# 2. Accept *args, **kwargs so the wrapper works for any function signature.
# 3. Return the result of fn(*args, **kwargs) unless you intentionally change it.
# 4. functools.wraps also sets __wrapped__, letting you access the original fn.
