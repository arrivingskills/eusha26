# Higher-order functions: map, filter, reduce, sorted with key functions
# A higher-order function either takes a function as an argument or returns one.

from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# --- map ---
# Applies a function to every item and returns an iterator.
squares = list(map(lambda x: x**2, numbers))
print("squares:", squares)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

words = ["hello", "world", "python"]
uppercased = list(map(str.upper, words))
print("uppercased:", uppercased)  # ['HELLO', 'WORLD', 'PYTHON']

# --- filter ---
# Keeps only items for which the function returns True.
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("evens:", evens)  # [2, 4, 6, 8, 10]

long_words = list(filter(lambda w: len(w) > 4, words))
print("long words:", long_words)  # ['hello', 'world', 'python']

# --- reduce ---
# Cumulatively applies a function to collapse a sequence to a single value.
total = reduce(lambda acc, x: acc + x, numbers)
print("sum:", total)  # 55

product = reduce(lambda acc, x: acc * x, [1, 2, 3, 4, 5])
print("product:", product)  # 120

# --- sorted with a key function ---
# key= accepts any callable; items are sorted by the value it returns.
people = [
    {"name": "Zara", "age": 30},
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 35},
]

by_age = sorted(people, key=lambda p: p["age"])
print("by age:", [p["name"] for p in by_age])  # ['Alice', 'Zara', 'Bob']

by_name = sorted(people, key=lambda p: p["name"])
print("by name:", [p["name"] for p in by_name])  # ['Alice', 'Bob', 'Zara']

# key= with a built-in
mixed = ["banana", "fig", "apple", "kiwi"]
by_length = sorted(mixed, key=len)
print("by length:", by_length)  # ['fig', 'kiwi', 'apple', 'banana']

# Combining: filter then sort
even_squares = sorted(
    map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers))
)
print("even squares sorted:", even_squares)  # [4, 16, 36, 64, 100]
