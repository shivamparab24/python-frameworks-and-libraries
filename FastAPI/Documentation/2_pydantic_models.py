# pydantic is a python library to perform data validation

# you declare the 'shape' of data as classes with attributes
# and each attribute has a type

# then you create a instance of that class with some values
# and it will validate the values, convert them to appropriate
# type (if specified) and give you an object with all the data




from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: datetime | None = None
    friends: list[int] = []


# external_data = {
#     "id": "123",
#     "signup_ts": "2017-06-01 12:22",
#     "friends": [1, "2", b"3"],
# }

external_data = {
    "id": 456, 
    "name": "Alice", # this should come instead of default value "John Doe"
    "signup_ts": "2018-12-31 12:23",
    "friends": [6, "6", b"12"],
}

user = User(**external_data)
print(user)
# > User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
print(user.id)
# > 123
print(type(user.friends))