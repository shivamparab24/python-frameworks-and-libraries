# the below function is a simple function deinition with 2 input parameters

def get_full_name(first_name, last_name):
    full_name = first_name.title() + " " + last_name.title()
    """
    title() method returns a string where the first character in every word is upper case
    """
    return full_name

print(get_full_name("hello", "world"))




# now we add type hints to parameters
# we use colon (:) and not equal (=) signs to denote type hints

def get_full_name1(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title()
    """
    you can see that after adding type hints (str) the string title() method has changed colour
    """
    return full_name

print(get_full_name1("hello", "world"))




def get_name_with_age(name: str, age: float):
    name_with_age = name + " is this old: " + str(age)
    """
    we need to convert 'age' to string
    """
    return name_with_age

print(get_name_with_age("python", "hello"))
print(get_name_with_age("python", 24))




# declaring types

# simple types (int, float, string, bool, bytes)
def get_items(item_a: str, item_b: int, item_c: float, item_d: bool, item_e: bytes):
    return item_a, item_b, item_c, item_d, item_e

# typing module
from typing import Any

def some_function(data: Any):
    print(data)


# generic types
# parameters that can take type params are called Generic types or Generics
# list, tuple, set, dict

# list
def process_items(items: list[str]): # this means the variable items is a list of strings
    """
    here 'str' is called type parameter which is passed to list
    """
    for item in items:
        print(item)


# tuple and set
def process_items1(items_t: tuple[int, int, str], items_s: set[bytes]):
    """
    items_t is a tuple with three items a int, another int and a str
    items_s is a set with items of type bytes
    """
    return items_t, items_s


# dict
def process_items2(prices: dict[str: float]):
    """
    the variable prices is a dict:
    - the keys of this dict are of type string
    - the values of this dict are of type float
    """
    for items_name, items_price in prices.items():
        print(items_name)
        print(items_price)


# union
def process_items3(item: int | str):
    """
    a variable can be declared any of several types
    we define it using a vertical bar (|) to separate both types
    this is called 'union' because the var can be anything in the union of those two sets of types
    this means the item couold be either a int or a str
    """
    print(item)


# possibly None
def say_hi(name: str | None = None):
    """
    using str | none instead of just str will ley the editor help
    you detect errors where you could be assuming that a value is
    always a str, when it could actually be None too
    """
    if name is not None:
        print(f"Hey! {name}!")
    else:
        print("Hello World")
print(f"this is say_hi func: {say_hi()}")







# classes as types
# you can declare a class as the type of a variable

class Person:
    def __init__(self, name: str):
        self.name = name

def get_person_name(one_person: Person) -> str:
    """
    notice that one_person is a instance of class called person
    it is a type hint
    which means the parameter should be a Person object
    """
    return one_person.name


"""
Why pass a Person object instead of just a string?

A function could technically accept a string directly:

    def get_name(name: str):
        return name

However, doing this loses the advantages of object-oriented design.

A Person object represents a real-world entity and can store multiple
related attributes together. For example:

    class Person:
        def __init__(self, name, age, email):
            self.name = name
            self.age = age
            self.email = email

Now a single object contains all information related to that person:

    Person
      ├── name
      ├── age
      └── email

By passing the Person instance to functions, we operate on the complete
entity instead of isolated pieces of data. This keeps related information
grouped together and makes programs easier to extend, maintain, and reason
about as the system grows.
"""



# Edge Case: When Adding New Attributes Can Break Existing Code

"""
In Python, a class can be extended by adding new attributes without
changing functions that only depend on existing attributes.

Example:

    class Person:
        def __init__(self, name: str):
            self.name = name

A function using this class might look like:

    def get_person_name(one_person: Person) -> str:
        return one_person.name

This function only relies on the presence of the attribute "name".

------------------------------------------------------------

Problem Scenario

If we modify the class constructor to require additional parameters:

    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

Then previously valid code will break:

    Person("Alice")

This fails because the constructor now requires an additional argument
("age"). Python will raise a TypeError since the required parameter
was not provided.

Important observation:

    The function get_person_name() still works correctly.

The issue is not with the function but with object creation. Any
location in the codebase that instantiates the Person class must now
provide the new argument.

------------------------------------------------------------

Common Solution: Provide Default Values

To maintain backward compatibility, new attributes are often given
default values.

    class Person:
        def __init__(self, name: str, age: int | None = None):
            self.name = name
            self.age = age

Now both of the following remain valid:

    Person("Alice")
    Person("Alice", 25)

This approach allows the class to evolve without breaking existing
code that already depends on the original constructor.

------------------------------------------------------------

Key Design Insight

When modifying class constructors in real systems, new parameters
should usually include default values. This preserves compatibility
with existing code while still allowing the class to be extended.
"""

# the functions becomes like this because name might be None
def get_person_name(one_person: Person) -> str | None:
    return one_person.name






# type hints with metadata annotations
from typing import Annotated

def say_hello(name: Annotated[str, "this is just metadata"]) -> str:
    """
    use this space in Annotated to provide FastAPI with additional
    metadata about how you want your application to behave.
    """
    return f"Hello {name}"

print(say_hello("Worls"))





# Type hints in FastAPI
# FastAPI takes advantage of these type hints to do several things.

# With FastAPI you declare parameters with type hints and you get:

# Editor support.
# Type checks.
# ...and FastAPI uses the same declarations to:

# Define requirements: from request path parameters, query parameters, headers, bodies, dependencies, etc.
# Convert data: from the request to the required type.
# Validate data: coming from each request:
# Generating automatic errors returned to the client when the data is invalid.
# Document the API using OpenAPI:
# which is then used by the automatic interactive documentation user interfaces.