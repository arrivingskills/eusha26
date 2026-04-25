# Common closure patterns: factory functions, accumulators, memoisation by hand

# ── 1. Factory function ────────────────────────────────────────────────────────
# A factory creates and returns specialised functions, each capturing its own
# configuration.


def make_multiplier(n):
    def multiply(x):
        return x * n

    return multiply


double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15


def make_validator(min_val, max_val):
    def validate(value):
        return min_val <= value <= max_val

    return validate


is_percentage = make_validator(0, 100)
is_byte = make_validator(0, 255)

print(is_percentage(75))  # True
print(is_percentage(120))  # False
print(is_byte(200))  # True


# ── 2. Accumulator ────────────────────────────────────────────────────────────
# Each call to the returned function updates and returns a running value.


def make_running_total():
    total = 0

    def add(n):
        nonlocal total
        total += n
        return total

    return add


running = make_running_total()
print(running(10))  # 10
print(running(5))  # 15
print(running(20))  # 35


def make_averager():
    values = []  # mutable objects don't need nonlocal

    def average(n):
        values.append(n)
        return sum(values) / len(values)

    return average


avg = make_averager()
print(avg(10))  # 10.0
print(avg(20))  # 15.0
print(avg(30))  # 20.0


# ── 3. Memoisation by hand ────────────────────────────────────────────────────
# Cache expensive results keyed by the arguments.


def make_memoised(fn):
    cache = {}

    def wrapper(*args):
        if args not in cache:
            print(f"  computing {fn.__name__}{args}…")
            cache[args] = fn(*args)
        else:
            print(f"  cache hit for {args}")
        return cache[args]

    return wrapper


def slow_square(n):
    return n * n


fast_square = make_memoised(slow_square)

print(fast_square(4))  # computing … → 16
print(fast_square(4))  # cache hit   → 16
print(fast_square(7))  # computing … → 49


# Recursive example: memoised Fibonacci
def make_fib():
    cache = {}

    def fib(n):
        if n in cache:
            return cache[n]
        if n <= 1:
            result = n
        else:
            result = fib(n - 1) + fib(n - 2)
        cache[n] = result
        return result

    return fib


fib = make_fib()
print([fib(n) for n in range(10)])  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
