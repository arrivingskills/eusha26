# Advanced Python Syllabus — Eusha

## Course Overview

A structured course covering advanced Python concepts: functional programming patterns, object-oriented design in depth, metaprogramming, and idiomatic Python. Each lesson is ~60–90 minutes with exercises to complete between sessions.

---

## Lesson 1: First-Class Functions & Closures

### Topics

- Functions as objects: assigning, passing, returning functions
- Higher-order functions: `map`, `filter`, `reduce`, `sorted` with key functions
- Closures: how inner functions capture enclosing scope
- The `nonlocal` keyword
- Common closure patterns: factory functions, accumulators, memoisation by hand

### Key Concepts

- A **closure** is a function that remembers the variables from its enclosing scope even after that scope has finished executing
- Python's late binding in closures (the loop variable gotcha)

### Exercises (between lessons)

1. **Multiplier factory** — Write a function `make_multiplier(n)` that returns a function which multiplies its argument by `n`.

   ```python
   double = make_multiplier(2)
   assert double(5) == 10
   assert double(3) == 6
   ```

2. **Running average** — Write a function `make_averager()` that returns a function. Each call to the returned function passes in a new number and returns the running average of all numbers seen so far.

   ```python
   avg = make_averager()
   assert avg(10) == 10.0
   assert avg(20) == 15.0
   assert avg(30) == 20.0
   ```

3. **Counter with reset** — Write `make_counter()` that returns a dict with two functions: `increment` and `reset`. `increment()` returns the next count each time, `reset()` sets it back to 0. Use `nonlocal`.

4. **Loop trap** — Predict the output of this code, then fix it using a closure:

   ```python
   funcs = []
   for i in range(5):
       funcs.append(lambda: i)
   print([f() for f in funcs])  # What prints? Why?
   ```

---

## Lesson 2: Decorators

### Topics

- What a decorator actually is (syntactic sugar for wrapping)
- Writing a basic decorator (with `functools.wraps`)
- Decorators that take arguments (decorator factories)
- Stacking multiple decorators (execution order)
- Class-based decorators (using `__call__`)
- Real-world examples: timing, logging, access control, retry logic

### Key Concepts

- `@decorator` is just `func = decorator(func)`
- `@decorator(args)` means `func = decorator(args)(func)` — the outer call returns the actual decorator
- Always use `@functools.wraps(fn)` to preserve the wrapped function's metadata

### Exercises (between lessons)

1. **Timer decorator** — Write `@timer` that prints how long a function took to execute.

   ```python
   @timer
   def slow_fn():
       import time; time.sleep(0.5)
   slow_fn()  # prints: slow_fn took 0.50s
   ```

2. **Call counter** — Write `@count_calls` that adds a `.call_count` attribute to the decorated function tracking how many times it's been called.

3. **Retry decorator** — Write `@retry(max_attempts=3, delay=1.0)` that re-runs a function if it raises an exception, up to `max_attempts` times, waiting `delay` seconds between attempts.

4. **Type checker** — Write `@enforce_types` that uses a function's type annotations to check argument types at call time and raises `TypeError` if they don't match.

   ```python
   @enforce_types
   def greet(name: str, times: int) -> str:
       return name * times
   greet("hi", 3)     # works
   greet("hi", "3")   # raises TypeError
   ```

5. **Memoisation** — Write `@memoize` that caches results based on arguments. Test it on a recursive Fibonacci function and observe the speedup.

---

## Lesson 3: Iterators, Generators & Lazy Evaluation

### Topics

- The iterator protocol: `__iter__` and `__next__`
- Writing custom iterator classes
- Generator functions (`yield`)
- Generator expressions vs list comprehensions
- `yield from` for delegation
- Infinite sequences and lazy pipelines
- `itertools` essentials: `chain`, `islice`, `groupby`, `product`, `combinations`, `takewhile`, `dropwhile`

### Key Concepts

- Generators are lazy — they produce values one at a time and don't hold the whole sequence in memory
- A generator function returns a generator object; calling `next()` on it resumes execution until the next `yield`

### Exercises (between lessons)

1. **Fibonacci generator** — Write a generator `fib()` that yields Fibonacci numbers indefinitely. Use `itertools.islice` to get the first 20.

2. **File chunker** — Write a generator `read_chunks(filepath, size=1024)` that yields chunks of a file without loading it all into memory.

3. **Flatten** — Write a generator `flatten(nested)` that takes an arbitrarily nested list and yields all scalar values.

   ```python
   assert list(flatten([1, [2, [3, 4], 5], 6])) == [1, 2, 3, 4, 5, 6]
   ```

4. **Pipeline** — Build a lazy data pipeline using generators: read lines from a file → filter lines containing a keyword → extract a field → convert to int → compute a running sum. No intermediate lists.

5. **Custom range** — Implement a class `FloatRange(start, stop, step)` that supports the iterator protocol and works in `for` loops, producing float values.

---

## Lesson 4: Advanced FP — Currying, Partial Application & Composition

### Topics

- Partial application with `functools.partial`
- Currying: what it is, manual implementation, automatic currying
- Function composition: building pipelines from small functions
- Writing a `compose` and `pipe` utility
- `operator` module: `itemgetter`, `attrgetter`, `methodcaller`
- Practical FP idioms in Python (when to use them, when not to)

### Key Concepts

- **Currying** transforms `f(a, b, c)` into `f(a)(b)(c)` — each call returns a new function expecting the next argument
- **Partial application** fixes some arguments and returns a new function expecting the rest
- **Composition** chains functions: `compose(f, g)(x)` = `f(g(x))`

### Exercises (between lessons)

1. **Manual curry** — Write a `curry` function that takes any function and returns its curried version.

   ```python
   @curry
   def add(a, b, c):
       return a + b + c
   assert add(1)(2)(3) == 6
   assert add(1, 2)(3) == 6
   assert add(1)(2, 3) == 6
   ```

2. **Compose & pipe** — Implement `compose(*fns)` (right-to-left) and `pipe(*fns)` (left-to-right).

   ```python
   transform = pipe(str.strip, str.lower, str.title)
   assert transform("  hello world  ") == "Hello World"
   ```

3. **Data processing with partial** — Given a list of dicts representing products, use `functools.partial`, `operator.itemgetter`, and `sorted` to create reusable sorters:

   ```python
   sort_by_price = partial(sorted, key=itemgetter('price'))
   sort_by_name = partial(sorted, key=itemgetter('name'))
   ```

4. **Point-free style** — Rewrite this function using only composition, partial application, and operator functions (no `lambda`, no `def`):

   ```python
   def process(items):
       return list(map(lambda x: x.strip().upper(), filter(lambda x: len(x) > 3, items)))
   ```

---

## Lesson 5: Advanced OOP — Dunder Methods & the Data Model

### Topics

- Python's data model (the "dunder" protocol)
- `__repr__`, `__str__`, `__format__`
- Comparison: `__eq__`, `__lt__`, `__hash__` and `functools.total_ordering`
- Arithmetic: `__add__`, `__radd__`, `__iadd__`
- Container protocol: `__len__`, `__getitem__`, `__contains__`, `__iter__`
- Context managers: `__enter__`, `__exit__`
- Callable objects: `__call__`
- `__slots__` for memory optimisation

### Exercises (between lessons)

1. **Vector class** — Implement a `Vector` class supporting addition, subtraction, scalar multiplication, dot product, magnitude, equality comparison, and a nice `repr`.

   ```python
   v1 = Vector(1, 2, 3)
   v2 = Vector(4, 5, 6)
   assert v1 + v2 == Vector(5, 7, 9)
   assert v1 * 3 == Vector(3, 6, 9)
   assert 3 * v1 == Vector(3, 6, 9)  # __rmul__
   assert abs(Vector(3, 4)) == 5.0
   ```

2. **Custom sequence** — Build a `SortedList` class that always keeps its elements sorted. Implement `__getitem__`, `__len__`, `__contains__` (using binary search), `__iter__`, `__repr__`, and an `add` method.

3. **Context manager** — Write a `TempDirectory` context manager class that creates a temporary directory on enter, yields its path, and deletes it (with all contents) on exit.

4. **Callable class** — Create a `Pipeline` class where you add processing steps and then call the instance to run data through all steps:

   ```python
   p = Pipeline()
   p.add_step(str.strip)
   p.add_step(str.upper)
   assert p("  hello  ") == "HELLO"
   ```

---

## Lesson 6: Descriptors, Properties & Attribute Access

### Topics

- The descriptor protocol: `__get__`, `__set__`, `__delete__`, `__set_name__`
- Data descriptors vs non-data descriptors
- How `property` works under the hood (it's a descriptor)
- Attribute lookup order: instance dict → class (data descriptors) → instance dict → class → `__getattr__`
- `__getattr__` vs `__getattribute__`
- Building reusable validation descriptors

### Key Concepts

- A **descriptor** is any object that defines `__get__`, `__set__`, or `__delete__`
- `property` is the most common descriptor — understanding it as a descriptor demystifies it
- `__set_name__` (Python 3.6+) lets the descriptor know what attribute name it was assigned to

### Exercises (between lessons)

1. **Validated fields** — Write descriptor classes `Positive`, `NonEmpty`, and `InRange(lo, hi)` that validate values on assignment:

   ```python
   class Product:
       name = NonEmpty()
       price = Positive()
       quantity = InRange(0, 1000)
   ```

2. **Lazy property** — Write a `lazy_property` descriptor that computes a value on first access and caches it on the instance (so subsequent access is fast and doesn't call the function again).

3. **Audit trail** — Write a descriptor `Tracked` that logs every get and set operation with timestamps.

4. **Implement property from scratch** — Write your own `MyProperty` class that behaves like the built-in `property`, supporting getter, setter, deleter, and the `@MyProperty` decorator syntax.

---

## Lesson 7: Metaclasses & Class Creation

### Topics

- `type` as a class factory: `type(name, bases, namespace)`
- `__class__`, `type()`, `isinstance()`, `issubclass()`
- `__init_subclass__` (the modern lightweight alternative to metaclasses)
- Metaclasses: `__new__` and `__init__` on the metaclass
- `__prepare__` for custom namespace (e.g., `OrderedDict`)
- Practical metaclass uses: registries, validation, ORMs, ABCs
- When to use metaclasses vs `__init_subclass__` vs class decorators

### Key Concepts

- A metaclass is the "class of a class" — it controls how classes themselves are created
- `class Foo(metaclass=Meta)` means `Meta('Foo', bases, namespace)` is called to create the class
- In most cases `__init_subclass__` or a class decorator is simpler and sufficient

### Exercises (between lessons)

1. **Plugin registry** — Using `__init_subclass__`, create a base class `Plugin` that automatically registers all subclasses in a `Plugin.registry` dict keyed by class name.

   ```python
   class MyPlugin(Plugin):
       pass
   assert 'MyPlugin' in Plugin.registry
   ```

2. **Singleton metaclass** — Write a metaclass `SingletonMeta` that ensures a class can only have one instance.

3. **Schema validation** — Write a metaclass that reads class-level type annotations and, in `__init__`, validates that all attributes match their declared types.

4. **Enum from scratch** — Using a metaclass with `__prepare__` returning a custom dict, implement a basic enum where duplicate values raise an error and members are accessible as class attributes.

5. **Class creation order** — Create a test file that prints messages from `__init_subclass__`, metaclass `__new__`, metaclass `__init__`, metaclass `__prepare__`, class `__init__`, and class `__new__`. Predict the output order, then run it and explain the results.

---

## Lesson 8: Concurrency — Threads, Async & the GIL

### Topics

- The GIL: what it is, why it exists, what it means for performance
- `threading`: threads, locks, `concurrent.futures.ThreadPoolExecutor`
- `multiprocessing` and `ProcessPoolExecutor` for CPU-bound work
- `asyncio` fundamentals: event loop, coroutines, `await`, `async for`, `async with`
- `asyncio.gather`, `asyncio.create_task`, `asyncio.Queue`
- Choosing the right concurrency model for the problem

### Key Concepts

- The GIL means only one thread runs Python bytecode at a time — threads help with I/O-bound work, not CPU-bound
- `async`/`await` is cooperative multitasking — a coroutine must explicitly `await` to yield control
- Use threads for I/O parallelism, processes for CPU parallelism, asyncio for high-concurrency I/O

### Exercises (between lessons)

1. **Parallel downloads** — Write a script that downloads 10 web pages concurrently using `ThreadPoolExecutor` and measures total time vs sequential.

2. **Async web scraper** — Rewrite the above using `asyncio` and `aiohttp`. Compare the approaches.

3. **Producer-consumer** — Implement a producer-consumer pattern with `asyncio.Queue`: one producer adds items, three consumers process them.

4. **Thread-safe counter** — Demonstrate a race condition with a shared counter and two threads, then fix it with a `Lock`.

5. **CPU benchmark** — Time a CPU-heavy task (e.g., computing primes) using: (a) sequential, (b) threading, (c) multiprocessing. Explain the results.

---

## Lesson 9: Error Handling, Context Managers & Protocols

### Topics

- Exception hierarchy and custom exceptions
- Exception chaining (`raise X from Y`)
- `contextlib`: `@contextmanager`, `suppress`, `ExitStack`, `closing`
- Structural pattern matching (Python 3.10+ `match`/`case`)
- Protocols and structural subtyping (`typing.Protocol`)
- Abstract base classes vs Protocols (nominal vs structural typing)
- Writing robust APIs with proper error hierarchies

### Exercises (between lessons)

1. **Exception hierarchy** — Design an exception hierarchy for a banking application: `BankError` → `InsufficientFunds`, `AccountNotFound`, `TransactionError`, `DailyLimitExceeded`. Use exception chaining where appropriate.

2. **Contextlib generators** — Rewrite the `TempDirectory` context manager from Lesson 5 using `@contextmanager`.

3. **ExitStack** — Write a function that opens a variable number of files and reads from all of them using `ExitStack`.

4. **Protocol class** — Define a `Drawable` protocol with a `draw(canvas)` method. Write functions that accept any `Drawable` and demonstrate that classes don't need to explicitly inherit from `Drawable` — just having the method is enough.

5. **Pattern matching** — Write a command parser using `match`/`case` that handles:

   ```python
   parse_command("quit")              # → Quit
   parse_command("move north 5")      # → Move(direction="north", steps=5)
   parse_command("attack goblin")     # → Attack(target="goblin")
   parse_command("use potion on self") # → Use(item="potion", target="self")
   ```

---

## Lesson 10: Putting It All Together — Project

### Project: Mini ORM

Build a small ORM (Object-Relational Mapper) that ties together most concepts from the course:

- **Metaclass or `__init_subclass__`** to register model classes and read field definitions
- **Descriptors** for field types with validation (`StringField`, `IntField`, `FloatField`)
- **Decorators** for query caching and logging
- **Closures / partial application** in query builder helpers
- **Generators** for lazy result iteration
- **Context manager** for database connection handling
- **Custom exceptions** for validation and query errors
- **Protocols** for pluggable backends (SQLite, in-memory dict)

```python
class User(Model):
    name = StringField(max_length=100)
    age = IntField(min_val=0)
    email = StringField()

# Usage
with Database("users.db") as db:
    db.create_table(User)
    db.insert(User(name="Eusha", age=25, email="eusha@example.com"))
    
    for user in db.select(User).where(age__gt=20):
        print(user)
```

### Milestones

1. Define `Field` descriptors with validation
2. Build the `Model` base class with metaclass/`__init_subclass__` for schema detection
3. Write the `Database` context manager with connection handling
4. Implement `insert` and `select` with lazy iteration
5. Add `where` filtering with closures
6. Add a `@cache_query` decorator
7. Define a `Backend` protocol and implement SQLite + in-memory backends
8. Write tests

---

## Recommended Schedule

| Week | Lesson | Topic |
|------|--------|-------|
| 1 | 1 | First-Class Functions & Closures |
| 2 | 2 | Decorators |
| 3 | 3 | Iterators, Generators & Lazy Evaluation |
| 4 | 4 | Currying, Partial Application & Composition |
| 5 | 5 | Dunder Methods & the Data Model |
| 6 | 6 | Descriptors, Properties & Attribute Access |
| 7 | 7 | Metaclasses & Class Creation |
| 8 | 8 | Concurrency |
| 9 | 9 | Error Handling, Context Managers & Protocols |
| 10–11 | 10 | Final Project: Mini ORM |

---

## Resources

- *Fluent Python* (2nd ed.) — Luciano Ramalho
- *Python Cookbook* (3rd ed.) — David Beazley & Brian K. Jones
- [Real Python — Advanced tutorials](https://realpython.com/)
- [Python docs — Data Model](https://docs.python.org/3/reference/datamodel.html)
- [Python docs — functools](https://docs.python.org/3/library/functools.html)
- [Python docs — itertools](https://docs.python.org/3/library/itertools.html)
