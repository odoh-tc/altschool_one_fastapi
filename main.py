from typing import Optional
from uuid import UUID
from fastapi import FastAPI, status, HTTPException


app = FastAPI()


class Student:
   def __init__(self, name, age, sex, height): 
        self.id = None
        self.name = name
        self.age = age
        self.sex = sex
        self.height = height




students = []

@app.get("/", status_code=status.HTTP_200_OK)
async def home():
    return {"message": "Hello, from the student API!"}


@app.get("/students", status_code=status.HTTP_200_OK)
async def get_all_students():
    return students


@app.get("/student/{id}", status_code=status.HTTP_200_OK)
async def get_a_student(id: str):  
    for student in students:
        if student.id == id:
            return student.__dict__
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

@app.get("/students/filtered", status_code=status.HTTP_200_OK)
async def get_many_students(min_age: int, max_age: int, limit: int = None, offset: int = 0):


    filtered_students = students

    print("Age attribute of students:")
    for student in filtered_students:
        print(student.age)


    if min_age is not None and max_age is not None:  
        filtered_students = [student for student in students if min_age <= student.age <= max_age]
    
    # filtered_students = filtered_students[offset:offset + limit] if limit is not None else filtered_students[offset:]
    if limit is not None:
        if limit > len(students):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Limit cannot exceed the total number of students")
        filtered_students = filtered_students[offset:offset + limit]
    else:
        filtered_students = filtered_students[offset:]
    return filtered_students


@app.post("/students", status_code=status.HTTP_200_OK)
async def create_student(name: str, age: int, sex: str, height: int):
    new_id = str(UUID(int=len(students) + 1))
    new_student = Student(name=name, age=age, sex=sex, height=height)
    new_student.id = new_id 
    students.append(new_student)
    return {"message": "Student successfully created.", "data":new_student.__dict__}














