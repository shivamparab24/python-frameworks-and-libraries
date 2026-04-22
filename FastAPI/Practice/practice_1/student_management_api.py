from fastapi import FastAPI, HTTPException

from FastAPI.Practice.practice_1.schema import Student
from FastAPI.Practice.practice_1.data import students_db

app = FastAPI()


# In-memory storage
current_id = 1



@app.post("/students")
def create_student(student: Student):

    new_id = max(students_db.keys()) + 1

    new_student = {
        "id": new_id,
        "name": student.name,
        "dept": student.dept,
        "subjects": student.subjects
    }

    students_db[new_id] = new_student

    return new_student



@app.get("/students")
def get_all():
    return list(students_db.values())


@app.get("/students/{id}")
def get_by_id(id: int):

    student = students_db.get(id)

    if student is None:
        raise HTTPException(
            status_code = 404,
            detail = "Student not Found"
        )
    
    return student

@app.put("/students/{id}")
def update_student(id: int, student: Student):

    if id not in students_db:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    
    students_db[id] = {
        "id": id,
        "name": student.name,
        "dept": student.dept,
        "subjects": student.subjects
    }

    return {"message": "Student updated successfully!!"}


@app.delete("/students/{id}")
def delete_student(id: int):
    
    if id not in students_db:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    
    del students_db[id]

    return {"message": "Student deleted successfully"}