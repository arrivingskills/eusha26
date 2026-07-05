class Pipeline:
    def __init__(self):
        self._steps = []

    def add_step(self, fn):
        if not callable(fn):
            raise TypeError("step must be callable")
        self._steps.append(fn)
        return self

    def __call__(self, value):
        for fn in self._steps:
            value = fn(value)
        return value


p = Pipeline()
p.add_step(str.strip)
p.add_step(str.upper)
assert p("  hello  ") == "HELLO"