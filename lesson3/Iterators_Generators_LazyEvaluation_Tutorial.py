
"""
Lesson 3: Iterators, Generators & Lazy Evaluation
==================================================
Topics covered:
  1. The iterator protocol: __iter__ and __next__
  2. Writing custom iterator classes
  3. Generator functions (yield)
  4. Generator expressions vs list comprehensions
  5. yield from for delegation
  6. Infinite sequences and lazy pipelines
  7. itertools essentials: chain, islice, groupby, product,
     combinations, takewhile, dropwhile
"""

import itertools


# ===========================================================================
# 1. THE ITERATOR PROTOCOL: __iter__ AND __next__
# ===========================================================================
# Any object that implements both __iter__() and __next__() is an iterator.
# __iter__ returns self (so the iterator is also iterable).
# __next__ returns the next value, or raises StopIteration when exhausted.

print("=" * 60)
print("1. THE ITERATOR PROTOCOL")
print("=" * 60)

# Python's for loop is just syntactic sugar for the iterator protocol.
# This:
#   for item in obj:
#       ...
# Is equivalent to:
#   it = iter(obj)           # calls obj.__iter__()
#   while True:
#       try:
#           item = next(it)  # calls it.__next__()
#       except StopIteration:
#           break

nums = [10, 20, 30]
it = iter(nums)          # get an iterator from the list

print(next(it))  # 10
print(next(it))  # 20
print(next(it))  # 30

try:
    print(next(it))      # raises StopIteration — the iterator is exhausted
except StopIteration:
    print("StopIteration raised — iterator exhausted")

print()


# ===========================================================================
# 2. WRITING CUSTOM ITERATOR CLASSES
# ===========================================================================
# Build an iterator from scratch by implementing __iter__ and __next__.

print("=" * 60)
print("2. CUSTOM ITERATOR CLASSES")
print("=" * 60)


class CountUp:
    """Counts from `start` up to (but not including) `stop`."""

    def __init__(self, start, stop):
        self.current = start
        self.stop = stop

    def __iter__(self):
        # Returning self makes the object both an iterable AND an iterator.
        return self

    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


counter = CountUp(1, 6)
print("CountUp(1, 6):", list(counter))   # [1, 2, 3, 4, 5]

# Works naturally in a for loop:
for n in CountUp(0, 4):
    print(n, end=" ")
print()

# ---- Separating the iterable from the iterator ----
# A cleaner design: the iterable creates a fresh iterator each time
# iter() is called, so you can loop over it multiple times.


class EvenNumbers:
    """Iterable of even numbers in [start, stop)."""

    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __iter__(self):
        # Return a *new* iterator object each time.
        return EvenNumbersIterator(self.start, self.stop)


class EvenNumbersIterator:
    def __init__(self, start, stop):
        # Round start up to the nearest even number.
        self.current = start if start % 2 == 0 else start + 1
        self.stop = stop

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += 2
        return value


evens = EvenNumbers(1, 12)
print("First pass:", list(evens))   # [2, 4, 6, 8, 10]
print("Second pass:", list(evens))  # [2, 4, 6, 8, 10] — works again!

print()


# ===========================================================================
# 3. GENERATOR FUNCTIONS (yield)
# ===========================================================================
# A generator function uses `yield` to produce values one at a time.
# Calling the function returns a generator object — nothing runs yet.
# Each call to next() resumes execution until the next `yield`.

print("=" * 60)
print("3. GENERATOR FUNCTIONS (yield)")
print("=" * 60)


def count_up(start, stop):
    """Generator equivalent of the CountUp class above."""
    current = start
    while current < stop:
        yield current        # pause here, send value to caller
        current += 1         # resume here on the next next() call


gen = count_up(1, 6)
print(type(gen))             # <class 'generator'>
print(list(gen))             # [1, 2, 3, 4, 5]


def fibonacci():
    """Yields Fibonacci numbers indefinitely."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# Generators are lazy — this infinite sequence produces no values
# until you ask for them.
fib_gen = fibonacci()
first_8 = [next(fib_gen) for _ in range(8)]
print("First 8 Fibonacci:", first_8)   # [0, 1, 1, 2, 3, 5, 8, 13]


def squares(n):
    """Yields 0², 1², 2², … (n-1)²."""
    for i in range(n):
        print(f"  computing {i}²...")
        yield i * i


print("Creating generator (nothing runs yet):")
sq = squares(4)
print("Calling next() — execution resumes until the next yield:")
print(next(sq))   # computes 0², yields 0
print(next(sq))   # computes 1², yields 1

print()


# ===========================================================================
# 4. GENERATOR EXPRESSIONS VS LIST COMPREHENSIONS
# ===========================================================================

print("=" * 60)
print("4. GENERATOR EXPRESSIONS VS LIST COMPREHENSIONS")
print("=" * 60)

import sys

# List comprehension — evaluates everything immediately, stores in memory.
squares_list = [x * x for x in range(10)]
print("List comprehension:", squares_list)
print("Size in memory:", sys.getsizeof(squares_list), "bytes")

# Generator expression — lazy; produces values on demand.
# Syntax: replace [] with ().
squares_gen = (x * x for x in range(10))
print("Generator expression:", squares_gen)
print("Size in memory:", sys.getsizeof(squares_gen), "bytes")   # much smaller!

# Both give the same values:
print("Values from genexp:", list(squares_gen))

# Generator expressions can be passed directly to functions that consume
# iterables — no extra parentheses needed when it's the only argument.
total = sum(x * x for x in range(100))
print("Sum of first 100 squares:", total)   # 328350

# When to use which:
#   - List comprehension: you need to access elements multiple times,
#     use indexing, or know the length.
#   - Generator expression: single-pass iteration, large / infinite data,
#     or chaining with other iterators.

print()


# ===========================================================================
# 5. yield from FOR DELEGATION
# ===========================================================================
# `yield from iterable` delegates to a sub-iterator.
# It is equivalent to: for item in iterable: yield item
# But it is faster and handles .send() / .throw() correctly.

print("=" * 60)
print("5. yield from FOR DELEGATION")
print("=" * 60)


def chain_manual(*iterables):
    """Chain iterables together — manual version."""
    for it in iterables:
        for item in it:
            yield item


def chain_yield_from(*iterables):
    """Chain iterables together — using yield from."""
    for it in iterables:
        yield from it           # delegates to each sub-iterator


print("chain_manual:", list(chain_manual([1, 2], [3, 4], [5])))
print("chain_yield_from:", list(chain_yield_from([1, 2], [3, 4], [5])))


def flatten(nested):
    """
    Recursively flatten an arbitrarily nested iterable using yield from.
    Yields scalar values in order.
    """
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)   # recurse into sub-lists
        else:
            yield item


nested = [1, [2, [3, 4], 5], [6, [7, [8]]]]
print("flatten:", list(flatten(nested)))   # [1, 2, 3, 4, 5, 6, 7, 8]


# yield from also works great for composing generators:
def first_n(gen, n):
    yield from itertools.islice(gen, n)   # see itertools section below


print("First 5 fibs via yield from:", list(first_n(fibonacci(), 5)))

print()


# ===========================================================================
# 6. INFINITE SEQUENCES AND LAZY PIPELINES
# ===========================================================================
# Generators shine when processing large (or infinite) streams of data.
# You compose small generator functions into a pipeline — data flows
# through one item at a time with minimal memory overhead.

print("=" * 60)
print("6. INFINITE SEQUENCES AND LAZY PIPELINES")
print("=" * 60)


# ---- Infinite counter ----
def naturals(start=0):
    """Yields 0, 1, 2, 3, … indefinitely."""
    n = start
    while True:
        yield n
        n += 1


# ---- Pipeline stages as generators ----
def take(n, iterable):
    """Yield only the first n items."""
    yield from itertools.islice(iterable, n)


def only_evens(iterable):
    """Filter: pass through only even numbers."""
    for n in iterable:
        if n % 2 == 0:
            yield n


def squared(iterable):
    """Transform: yield each value squared."""
    for n in iterable:
        yield n * n


# Build the pipeline — nothing is computed yet:
pipeline = squared(only_evens(take(20, naturals())))

# Consume it — data flows through all stages lazily:
result = list(pipeline)
print("First 20 naturals → evens → squared:", result)
# [0, 4, 16, 36, 64, 100, 144, 196, 256, 324]


# ---- Real-world style: processing "log lines" ----
def fake_log_lines():
    """Simulates an infinite stream of log lines."""
    import random
    levels = ["INFO", "WARNING", "ERROR"]
    messages = ["connected", "timeout", "disk full", "ok", "retry"]
    n = 0
    while True:
        yield f"{random.choice(levels)} - event {n}: {random.choice(messages)}"
        n += 1


def filter_level(level, lines):
    for line in lines:
        if line.startswith(level):
            yield line


def extract_message(lines):
    for line in lines:
        yield line.split(": ", 1)[1]   # everything after the first ": "


# Pipeline: take 100 log lines → keep ERRORs → extract message text
error_messages = list(
    extract_message(
        filter_level("ERROR",
                     take(100, fake_log_lines()))
    )
)
print(f"ERROR messages from 100 log lines ({len(error_messages)} found):")
for msg in error_messages[:3]:
    print(" ", msg)

print()


# ===========================================================================
# 7. itertools ESSENTIALS
# ===========================================================================

print("=" * 60)
print("7. itertools ESSENTIALS")
print("=" * 60)

# ---- chain ----------------------------------------------------------------
# Concatenate multiple iterables into one sequence.

from itertools import chain

letters = chain("ABC", "DEF", [1, 2, 3])
print("chain:", list(letters))   # ['A', 'B', 'C', 'D', 'E', 'F', 1, 2, 3]

# chain.from_iterable — flatten one level from an iterable of iterables:
nested_lists = [[1, 2], [3, 4], [5, 6]]
print("chain.from_iterable:", list(chain.from_iterable(nested_lists)))

print()

# ---- islice ---------------------------------------------------------------
# Slice any iterable (including infinite ones) without materialising it.

from itertools import islice

# islice(iterable, stop)
# islice(iterable, start, stop[, step])
first_10_fibs = list(islice(fibonacci(), 10))
print("First 10 Fibonacci:", first_10_fibs)

every_other = list(islice(range(20), 0, 20, 2))
print("Every other from range(20):", every_other)

print()

# ---- groupby --------------------------------------------------------------
# Group consecutive elements by a key function.
# IMPORTANT: the input must be sorted by the key first.

from itertools import groupby

words = ["ant", "bee", "cat", "bear", "ape", "crow", "cod"]
words.sort(key=lambda w: w[0])   # sort by first letter

print("groupby first letter:")
for letter, group in groupby(words, key=lambda w: w[0]):
    print(f"  {letter!r}: {list(group)}")

# Grouping numbers by even/odd:
data = sorted([1, 4, 2, 8, 5, 3, 6, 7], key=lambda n: n % 2)
for parity, group in groupby(data, key=lambda n: "even" if n % 2 == 0 else "odd"):
    print(f"  {parity}: {list(group)}")

print()

# ---- product --------------------------------------------------------------
# Cartesian product — like nested for loops.

from itertools import product

coords = list(product([0, 1], repeat=2))
print("product([0,1], repeat=2):", coords)   # all 2-bit combos

suits = ["♠", "♥"]
ranks = ["A", "K", "Q"]
cards = list(product(ranks, suits))
print("Cards sample:", cards)

print()

# ---- combinations ---------------------------------------------------------
# All r-length combinations (no repetition, order doesn't matter).
# combinations_with_replacement allows repeats.

from itertools import combinations, combinations_with_replacement

players = ["Alice", "Bob", "Carol", "Dave"]
matchups = list(combinations(players, 2))
print("Round-robin matchups:", matchups)
print(f"  ({len(matchups)} games)")

dice_pairs = list(combinations_with_replacement([1, 2, 3, 4, 5, 6], 2))
print(f"Unique dice pairs: {len(dice_pairs)}")   # 21

print()

# ---- takewhile ------------------------------------------------------------
# Yield items while the predicate is True; stop at the first False.

from itertools import takewhile

data = [2, 4, 6, 7, 8, 10]
print("takewhile(even):", list(takewhile(lambda n: n % 2 == 0, data)))
# [2, 4, 6]  — stops as soon as 7 is encountered

# Useful for reading from a sorted / ordered stream:
ascending = [1, 3, 5, 4, 6, 8]   # stops when the sequence stops going up
print("takewhile ascending:", list(takewhile(
    lambda pair: pair[1] >= pair[0],
    zip(ascending, ascending[1:])
)))

print()

# ---- dropwhile ------------------------------------------------------------
# Skip items while the predicate is True; yield everything after.

from itertools import dropwhile

data = [1, 3, 5, 6, 7, 8, 9]
print("dropwhile(odd):", list(dropwhile(lambda n: n % 2 != 0, data)))
# [6, 7, 8, 9] — skips 1, 3, 5 then yields everything from 6 onward

log_lines = [
    "INFO  system starting",
    "INFO  loading config",
    "ERROR disk full",
    "INFO  retrying",
    "ERROR timeout",
]
# Skip INFO lines at the start, yield from the first ERROR onward:
from_first_error = list(dropwhile(lambda l: l.startswith("INFO"), log_lines))
print("From first ERROR:", from_first_error)

print()


# ===========================================================================
# PUTTING IT ALL TOGETHER — a lazy data pipeline using itertools
# ===========================================================================

print("=" * 60)
print("PUTTING IT ALL TOGETHER")
print("=" * 60)


def integers_from(n):
    while True:
        yield n
        n += 1


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


# Lazy pipeline:
#   naturals → keep primes → take first 15 → square them
prime_squares = list(
    islice(
        (p * p for p in integers_from(2) if is_prime(p)),
        15
    )
)
print("Squares of first 15 primes:", prime_squares)

# Group those squared primes by their last digit:
prime_squares.sort(key=lambda n: n % 10)
print("\nGrouped by last digit:")
for digit, group in groupby(prime_squares, key=lambda n: n % 10):
    print(f"  ends in {digit}: {list(group)}")
