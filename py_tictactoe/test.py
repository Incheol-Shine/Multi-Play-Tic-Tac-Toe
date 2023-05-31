from typing import NamedTuple

class Person(NamedTuple):
    name: str
    age: int
    height: float
    weight: float
    country: str = "Canada"


print(issubclass(Person, tuple))

jane = Person("Jane", 25, 1.75, 67)
jane.country = "America"
print(jane)
