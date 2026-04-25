# Closures
# A closure is a function that captures variables from its enclosing scope,
# keeping them alive even after the enclosing function has returned.

# --- Basic closure ---
def make_greeting(greeting):
    # 'greeting' is a free variable captured by the inner function
    def greet(name):
        return f"{greeting}, {name}!"

    return greet


hello = make_greeting("Hello")
hi = make_greeting("Hi")

print(hello("Eusha"))  # Hello, Eusha!
print(hi("Eusha"))  # Hi, Eusha!

# Each closure has its own independent copy of the captured variable
print(hello.__closure__[0].cell_contents)  # Hello
print(hi.__closure__[0].cell_contents)  # Hi


# --- What the closure "remembers" ---
def make_adder(n):
    def add(x):
        return x + n  # n is captured from make_adder's scope

    return add


add5 = make_adder(5)
add10 = make_adder(10)

print(add5(3))  # 8
print(add10(3))  # 13

# --- Late binding gotcha ---
# Python closures capture the *variable*, not the value at the time of creation.
# This causes a classic bug in loops:

funcs_buggy = []
for i in range(5):
    funcs_buggy.append(lambda: i)  # all lambdas capture the same 'i'

print([f() for f in funcs_buggy])  # [4, 4, 4, 4, 4]  — all see i=4

# Fix: bind the value immediately using a default argument
funcs_fixed = []
for i in range(5):
    funcs_fixed.append(
        lambda i=i: i
    )  # i=i creates a new local 'i' per iteration

print([f() for f in funcs_fixed])  # [0, 1, 2, 3, 4]


# Alternative fix: use a factory closure
def make_func(i):
    def fn():
        return i

    return fn


funcs_factory = [make_func(i) for i in range(5)]
print([f() for f in funcs_factory])  # [0, 1, 2, 3, 4]
