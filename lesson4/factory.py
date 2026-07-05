# abstract_factory_classmethod.py
"""
Demonstrates: Abstract superclass with a @classmethod factory method
that instantiates one of its concrete subclasses, each of which
honours the same interface (contract) but behaves differently.

Pattern summary
---------------
  AbstractShape.create(kind)   ← single entry-point (factory classmethod)
       │
       ├─► Circle      – area = π r²
       ├─► Rectangle   – area = w × h
       └─► Triangle    – area = ½ b h
"""
import math
from abc import ABC, abstractmethod


# ── Abstract base class ───────────────────────────────────────────────────────

class Shape(ABC):
    """Abstract superclass that defines the contract every shape must honor."""

    # ── Factory classmethod ───────────────────────────────────────────────────

    @classmethod
    def create(cls, kind: str, **kwargs) -> "Shape":
        """
        Instantiate and return the concrete subclass that matches *kind*.

        Usage
        -----
        circle    = Shape.create("circle",    radius=5)
        rectangle = Shape.create("rectangle", width=4, height=6)
        triangle  = Shape.create("triangle",  base=3,  height=8)
        """
        registry: dict[str, type[Shape]] = {
            "circle":    Circle,
            "rectangle": Rectangle,
            "triangle":  Triangle,
        }
        key = kind.strip().lower()
        if key not in registry:
            available = ", ".join(sorted(registry))
            raise ValueError(
                f"Unknown shape '{kind}'. Available kinds: {available}"
            )
        return registry[key](**kwargs)

    # ── Abstract contract (every subclass MUST implement these) ──────────────

    @abstractmethod
    def area(self) -> float:
        """Return the area of the shape."""

    @abstractmethod
    def perimeter(self) -> float:
        """Return the perimeter of the shape."""

    @abstractmethod
    def describe(self) -> str:
        """Return a human-readable description including measurements."""

    # ── Concrete shared behaviour ─────────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}  "
            f"area={self.area():.4f}  "
            f"perimeter={self.perimeter():.4f}"
        )


# ── Concrete subclasses ───────────────────────────────────────────────────────

class Circle(Shape):
    def __init__(self, radius: float) -> None:
        if radius <= 0:
            raise ValueError("radius must be positive")
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius

    def describe(self) -> str:
        return (
            f"Circle  radius={self.radius}  "
            f"area={self.area():.4f}  "
            f"circumference={self.perimeter():.4f}"
        )


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

    def describe(self) -> str:
        return (
            f"Rectangle  width={self.width}  height={self.height}  "
            f"area={self.area():.4f}  "
            f"perimeter={self.perimeter():.4f}"
        )


class Triangle(Shape):
    def __init__(self, base: float, height: float) -> None:
        if base <= 0 or height <= 0:
            raise ValueError("base and height must be positive")
        self.base = base
        self.height = height

    def area(self) -> float:
        return 0.5 * self.base * self.height

    def perimeter(self) -> float:
        # Assumes a right triangle for a deterministic perimeter
        hypotenuse = math.hypot(self.base, self.height)
        return self.base + self.height + hypotenuse

    def describe(self) -> str:
        return (
            f"Triangle  base={self.base}  height={self.height}  "
            f"area={self.area():.4f}  "
            f"perimeter={self.perimeter():.4f}"
        )


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    shapes = [
        Shape.create("circle",    radius=5),
        Shape.create("rectangle", width=4, height=6),
        Shape.create("triangle",  base=3,  height=8),
    ]

    print("=== Shapes created via Shape.create() factory classmethod ===\n")
    for shape in shapes:
        print(shape.describe())
        print(f"  → repr : {shape!r}\n")

    # Polymorphic processing — caller only knows about the Shape contract
    print("=== Polymorphic area sum ===")
    total_area = sum(s.area() for s in shapes)
    print(f"Total area of all shapes: {total_area:.4f}")

    # Error handling
    print("\n=== Error handling ===")
    try:
        Shape.create("hexagon", side=3)
    except ValueError as exc:
        print(f"Caught expected error: {exc}")