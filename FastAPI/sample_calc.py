from fastapi import FastAPI, HTTPException, status

app = FastAPI()

@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}

@app.get("/subtract")
def subtract(a: int, b: int):
    return {"result": a - b}

@app.get("/multiply")
def multiply(a: int, b: int):
    return {"result": a * b}

@app.get("/divide")
def divide(a: int, b: int):
    if b == 0:
        # return {"error": "division by zero"}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Division by zero"
        )
    return {"result": a / b}











# from fastapi import FastAPI
# import time
# import asyncio

# app = FastAPI()

# @app.get("/sync")
# def sync_example():
#     time.sleep(5)   # blocking
#     return {"message": "finished sync task"}


# @app.get("/async")
# async def async_example():
#     await asyncio.sleep(5)   # non-blocking
#     return {"message": "finished async task"}










# a = []
# b = [1,2,3,4,5,6]
# a = b

# a.append(7)

# print(b)
# print(a)




# a = []
# b = [1,2,3,4,5,6]
# a = b.copy()
# a.append(7)

# print(b)
# print(a)



# b = [1,2,3]
# a = b

# print(id(a))
# print(id(b))



# b = [1,2,3]
# a = b.copy()

# print(id(a))
# print(id(b))



# x = 10
# x = "hello"
# print(x)



# print(3 / 6)
# print(6 / 3)
# print(6 // 3)



# a = 5.0
# b = 2

# print(a / b) 
# print(a // b)


# print(0.1 + 0.2)


# is_valid = True
# is_empty = False



# print(is_empty)
# print(is_valid)


# word = "shivam"

# print(word[0:3])



# a = [1,2,3,4,5]

# a.pop(3)
# print(a)

# n = list(range(5))
# print(n)



# def is_palindrome(s: str):
#     left = 0
#     right = len(s) - 1

#     while left < right:
#         if s[left] != s[right]:
#             return False

#         left = left + 1
#         right = right - 1
    
#     return True


# print(is_palindrome("ogo"))



# a = [1,2,3]
# a.append(4)
# print(a)

# a.extend([5,6])
# print(a)

# a.extend([7])
# print(a)

# a.extend(8)
# print(a)


# a = [1,2,3]
# a.pop()
# print(a)

# a.pop(1)
# print(a)


# s = ["a", "b", "z", "f", "t", "u"]

# s.sort()
# print(s)

# s.sort(reverse=True)
# print(s)




# a = [1,2,3,4,5,6]
# b = [6,5,4,3,2,0]


# if a[::1] == b[::-1]:
#     print("True")
# else:
#     print("False")






# t = ("a", "b")

# t2 = t * 3
# print(t2)
# print()
# t = t
# print(t)


# user = {
#     "name": "Shivam",
#     "age": 25,
#     "city": "Pune"
# }

# print(user["name"])

# del user["name"]

# print(user)


# for i in range(10):
#     print(i)


# names = ["Alice","Bob","Charlie"]
# scores = [85,90,95]

# combined = zip(names, scores)

# x = list(combined)

# print(type(x))



# name = "slice"

# name2 = name[::-1]

# # for i in name:
# #     print(i)

# print(name2)



# nums = [1,2,3]

# it = iter(nums)
# print(it)


# nums = [1,2,3]

# it = iter(nums)

# print(next(it))
# print(next(it))
# print(next(it))



class Dog:
    species = "Canine"

    def __init__(self, name):
        self.name = name
        
d1 = Dog("Rocky")
d2 = Dog("Max")


print(Dog.species)
print(d1.species)