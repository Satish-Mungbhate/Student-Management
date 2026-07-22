from fastapi import FastAPI
import psycopg2
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    #allowed origins can be specified here
    allow_credentials=False, #supports cookies, authorization headers, etc.
    allow_methods=["*"],    #allowed methods can be specified here
    allow_headers=["*"]     #allowed headers can be specified here
)

'''
@app.get("/")
async def home():
    return {
        "message": "This is Home Page"
    }

@app.get("/users")
async def read_users():
    return {
        "message": "This is Users Data"
    }
    '''

# Database Connection
'''
connection = psycopg2.connect(
    host = os.getenv("HOST"),
    database = os.getenv("DATABASE"),
    user = os.getenv("USER"),
    password = os.getenv("PASSWORD")
)
'''
connection = psycopg2.connect(os.getenv("DATABASE_URL"))

cursor = connection.cursor()

#class Base Validation Model
class Student(BaseModel):
    id: int = None
    name: str = None
    cource: str = None
    

#Get All Students
@app.get("/students")
def get_students():
    #pass
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    #return {"students": students}
    #print(students)
    student_list = []
    for student in students:
        student_dict = {
            "id": student[0],
            "name": student[1],
            "cource": student[2],
        }
        student_list.append(student_dict)
    return student_list

#Get Student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int):
    #print(student_id)
    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cursor.fetchone()
    if student:
        return {
            "id": student[0],
            "name": student[1],
            "cource": student[2]
        }
    return {"error": "Student not found"}

#Create New Student Record
@app.post("/students")
def create_student(student: Student):
    #print(student.id, student.name, student.cource)
    cursor.execute("INSERT INTO students VALUES (%s, %s, %s)", (student.id, student.name, student.cource))
    connection.commit()
    return {
        "message": "Record inserted Successfully"
    }

# Replace Student Record
@app.put("/students/{id}")
def update_student(id: int, student: Student):
    #cursor.execute("UPDATE students SET id=%s, name = %s, cource = %s WHERE id = %s", (student.id, student.name, student.cource, id))
    cursor.execute("UPDATE students SET name = %s, cource = %s WHERE id = %s", (student.name, student.cource, id))
    connection.commit()
    return {
        "message": "Record updated Successfully"
    }

# Update Student Record
@app.patch("/students/{id}")
def patch_student(id: int, student: Student):
    if student.id != None:
        cursor.execute("UPDATE students SET id = %s WHERE id = %s", (student.id, id))
    if student.name != None:
        cursor.execute("UPDATE students SET name = %s WHERE id = %s", (student.name, id))
    if student.cource != None:
        cursor.execute("UPDATE students SET cource = %s WHERE id = %s", (student.cource, id))
    connection.commit()
    return {
        "message": "Record updated Successfully"
    }

# Delete Student Record by ID
@app.delete("/students/{id}")
def delete_student(id: int):
    cursor.execute("DELETE FROM students WHERE id = %s", (id,))
    connection.commit()
    return {
        "message": "Record deleted Successfully"
    }