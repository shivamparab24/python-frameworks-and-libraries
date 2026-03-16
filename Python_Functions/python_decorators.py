def changecase(func):
  def myinner():
    return func().upper()
  return myinner


def myfunction():
  return "Hello Sally"

print(myfunction())


@changecase
def myfunction1():
  return "Hello Sally"

print(myfunction1()) 


@changecase
def yourfunction():
  return "I am speed!"

print(yourfunction())










print("\n\n")
def decorator(func):
    def wrapper():
        print("Before calling the function.")
        func()
        print("After calling the function.")
    return wrapper

@decorator # Applying the decorator to a function
def greet():
    print("Hello, World!")
greet()





print("\n")
# arguments in decorated function
def changcase2(func):
   def inner(x):
      return func(x).upper()
   return inner

@changcase2
def myfunct(nam):
   return "Hello " + nam

print(myfunct("Namibia"))




print("\n")
# *args and **kwargs
def changecase(func):
  def myinner(*args, **kwargs):
    return func(*args, **kwargs).upper()
  return myinner

@changecase
def myfunction(nam):
    return "Hello " + nam

print(myfunction("John"))

"""
*args accepts any positional argument
**kwargs accepts any keyword argument
"""



print("\n")
# decorator with arguments
def changecase(n):
  def changecase(func):
    def myinner():
      if n == 1:
        a = func().lower()
      else:
        a = func().upper()
      return a
    return myinner
  return changecase

@changecase(1)
def myfunction():
  return "Hello Linus"

print(myfunction())




print("\n")
# mutiple decorators
def changecase(func):
  def myinner():
    return func().upper()
  return myinner

def addgreeting(func):
  def myinner():
    return "Hello " + func() + " Have a good day!"
  return myinner

@changecase
@addgreeting
def myfunction():
  return "Tobias"

print(myfunction())





print("\n")
# preserving function metadata
def changecase(func):
  def myinner():
    return func().upper()
  return myinner

@changecase
def myfunction():
  return "Have a great day!"

print(myfunction)
print(myfunction())
print(myfunction.__name__) #myinner





# Import functools.wraps to preserve the original function name and docstring.
print("\n\n")

import functools

def changecase(func):
  @functools.wraps(func)
  def myinner():
    return func().upper()
  return myinner

@changecase
def myfunction():
  return "Have a great day!"

print(myfunction.__name__) #myfucntion






print("\n\n\n")

import time
import datetime
from datetime import timedelta

def total_time(base_fn):
    def enhanced_fn(*args, **kwargs): #here *args works as a positional arguments -> arg = ("green", 1)............ similar for kwargs
        start_time = time.time()
        result_time = base_fn(*args, **kwargs) # here *args works as a unpacking -> base_fn("green", 1)........... similar for kwargs
        end_time = time.time()
        print(f"Task time: {end_time - start_time} seconds")
        return result_time
    return enhanced_fn


@total_time #comment this and uncomment below mentioned
def brew_tea(tea_type, sleep_time):
    print(f"Brewing {tea_type} tea...")
    time.sleep(sleep_time)
    print("Tea is ready...")


@total_time
def brew_matcha():
    print("Brewing matcha...")
    time.sleep(1)
    print("Matcha is ready...")
    return f"Drink matcha by {datetime.datetime.now() + timedelta(minutes=30)}"

# brew_tea = total_time(brew_tea) #uncomment this 
brew_tea("green", 3)
print()
brew_tea(tea_type = "Chai", sleep_time = 2)
print()
brew_matcha()
print()
print(brew_matcha())
# print()
# print(total_time(brew_tea))







print("\n")
""" Built in DECORATORS"""

"""@staticmethod"""

class MathOperations:
    @staticmethod
    def add(x, y):
        return x + y

# Using the static method
res = MathOperations.add(5, 3)
print("Using Static: ", res)

# Using object (instance)
obj = MathOperations()
res2 = obj.add(5, 3)
print("Using object: ", res2)


print("\n")

"""@classmethod"""

class Employee:
    raise_amount = 1.054
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        
    @classmethod
    def set_raise_amount(cls, amount):
        cls.raise_amount = amount

# Using the class method
print("Before @classmethod: ", Employee.raise_amount)
Employee.set_raise_amount(1.1000001)
print("After @classmethod: ", Employee.raise_amount)




print("\n")


"""@property"""

class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value >= 0:
            self._radius = value
        else:
            raise ValueError("Radius cannot be negative")

    @property
    def area(self):
        return 3.14159 * (self._radius ** 2)

# Using the property
c = Circle(5)
print(c.radius) 
print(c.area)    
c.radius = 10
print(c.area)



print("\n")
# withoit using @property
class Circle:
    def __init__(self, radius):
        self._radius = radius

    # getter
    def get_radius(self):
        return self._radius

    # setter
    def set_radius(self, value):
        if value >= 0:
            self._radius = value
        else:
            raise ValueError("Radius cannot be negative")

    # method instead of property
    def get_area(self):
        return 3.14159 * (self._radius ** 2)


# Using the class
c = Circle(5)

print(c.get_radius())
print(c.get_area())

c.set_radius(10)

print(c.get_area())