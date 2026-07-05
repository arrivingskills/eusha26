"""
This example works by combining a metaclass with descriptors to automatically
capture and validate class data.The Metaclass (ModelMeta) intercepts the class
definition to scan for any attributes defined as a Field. It gives each field
its own name context and stores them all in a hidden checklist (_fields).

The Base Class (BaseModel) uses that checklist inside its __init__ method to
automatically assign values and ensure no required fields are missing.

The Descriptors (Field) act as strict gatekeepers, triggering their __set__
method whenever a value is modified or assigned to instantly block any data
that does not match the required type.
"""

# 1. Field Descriptors for Type Checking
class Field:
    def __init__(self, expected_type):
        self.expected_type = expected_type
        self.name = None  # Will be set dynamically by the metaclass

    def __set__(self, instance, value):
        # Enforce type checking at runtime
        if not isinstance(value, self.expected_type):
            raise TypeError(f"Property '{self.name}' must be of type {self.expected_type.__name__}, got {type(value).__name__}")
        instance.__dict__[self.name] = value

# 2. The Metaclass
class ModelMeta(type):
    def __new__(cls, name, bases, dct):
        # Keep track of all fields defined on this class
        fields = {}

        # Scan through the class attributes
        for attr_name, attr_value in dct.items():
            if isinstance(attr_value, Field):
                attr_value.name = attr_name  # Give the field its name context
                fields[attr_name] = attr_value

        # Save the discovered fields into a special hidden class attribute
        dct['_fields'] = fields

        return super().__new__(cls, name, bases, dct)

# 3. Base Model Class
class BaseModel(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        # Automatically populate fields from keyword arguments
        for field_name in self._fields:
            if field_name not in kwargs:
                raise ValueError(f"Missing required field: '{field_name}'")
            setattr(self, field_name, kwargs[field_name])

    def serialize(self):
        # Instantly export the object to a clean dictionary format
        return {field_name: getattr(self, field_name) for field_name in self._fields}


# ---
# Define a strict database/API payload schema
class UserRegistration(BaseModel):
    username = Field(str)
    age = Field(int)
    is_admin = Field(bool)

# --- SUCCESS CASE ---
print("Creating a valid user...")
user = UserRegistration(username="tech_wizard", age=28, is_admin=False)
print("Serialized Data:", user.serialize())

# --- FAILURE CASE 1: Bad Type ---
print("\nTrying to inject an invalid type (string instead of integer for age)...")
try:
    bad_user = UserRegistration(username="hacker", age="twenty-eight", is_admin=False)
except TypeError as error:
    print("Caught Error:", error)

# --- FAILURE CASE 2: Missing Field ---
print("\nTrying to create a user with a missing field...")
try:
    incomplete_user = UserRegistration(username="ghost")
except ValueError as error:
    print("Caught Error:", error)
