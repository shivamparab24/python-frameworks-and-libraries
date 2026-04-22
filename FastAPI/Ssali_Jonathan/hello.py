from fastapi import FastAPI, Query, Header
from typing import List
from pydantic import BaseModel



app = FastAPI()

# @app.post("/")
@app.post("/")
async def hello():
    return {"message" : "Hello World!!"}



# if i ask for {name} i cannot specify key value in postman
@app.post("/greet/{name}")
async def greet_name(name: str) -> dict:
    return {"message" : f"Hello {name}"}


# # using below code i can specify key value  to postman
# @app.get("/greet")
# async def greet_name(name: str):
#     return {"message": f"Hello {name}"}


# for giving multiple requests on postman
@app.post("/greet")
async def greet_name(name: List[str]):
    return {"message": [f"Hello {n}" for n in name]}


@app.post("/greet")
async def greet_name(name: List[str] = Query(None)):
    return {"message": [f"Hello {n}" for n in name]}




# @app.post("/age_greet")
# async def age_greet(name: str, age: int):
#     return {"message": f"Hello {name}, You are {age} years old..."}


class Person(BaseModel):
    name: str
    age: int


@app.post("/age_greet")
async def age_greet(person: List[Person]):
    messages = [
        f"Hello {p.name}, You are {p.age} years old"
        for p in person
    ]
    return {"messages": messages}


class BookCreate(BaseModel):
    title : str
    author : str

@app.post("/create_book")
async def create_book(book_data: BookCreate):
    return {
        "title" : book_data.title,
        "author" : book_data.author
    }


@app.post("/get_headers")
async def get_headers(
    accept :str = Header(None),
    content_type : str = Header(None),
    user_agent :str = Header(None),
    host : str = Header(None)
):
    request_headers = {}

    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type
    request_headers["User-Agent"] = user_agent
    request_headers["Host"] = host
    
    return request_headers