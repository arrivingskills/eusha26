# The nonlocal keyword
# Inside a nested function, assignment creates a *new local* variable by default.
# 'nonlocal' tells Python to look in the enclosing (but non-global) scope instead,
# allowing the inner function to *rebind* the outer variable.

# --- Without nonlocal: assignment creates a local variable ---
def broken_counter():
    count = 0

    def increment():
        count = (
            count + 1
        )  # UnboundLocalError: 'count' referenced before assignment

    return increment


# broken_counter()()   # would raise UnboundLocalError


# --- With nonlocal: rebinds the enclosing variable ---
def make_counter():
    count = 0

    def increment():
        nonlocal count  # now refers to make_counter's 'count'
        count += 1
        return count

    return increment


counter = make_counter()
print(counter())  # 1
print(counter())  # 2
print(counter())  # 3

# Each call to make_counter produces an independent counter
other = make_counter()
print(other())  # 1  — completely independent from 'counter'
print(counter())  # 4  — 'counter' keeps its own state


# --- nonlocal across multiple levels ---
def outer():
    x = 10

    def middle():
        nonlocal x
        x += 5  # modifies outer's x

        def inner():
            nonlocal x
            x *= 2  # also modifies outer's x

        inner()
        return x

    return middle


fn = outer()
print(fn())  # (10 + 5) * 2 = 30

# --- Contrast: global vs nonlocal ---
total = 0


def add_to_total(n):
    global total  # 'global' reaches module-level scope
    total += n


add_to_total(10)
add_to_total(5)
print("global total:", total)  # 15
# Prefer nonlocal over global; nonlocal keeps state encapsulated.
