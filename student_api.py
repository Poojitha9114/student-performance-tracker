from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()

DATA_FILE = "students_data.json"

def load_students():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return {int(k): v for k, v in data.items()}
    return {}

def save_students(students):
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=2)

students = load_students()

class Student(BaseModel):
    name: str
    age: int
    marks: float
    subject: str

@app.post("/add-student")
def add_student(roll_no: int, student: Student):
    if roll_no in students:
        return {"error": "Student with this roll number already exists"}
    
    if student.marks >= 90:
        grade = "A"
    elif student.marks >= 75:
        grade = "B"
    elif student.marks >= 60:
        grade = "C"
    else:
        grade = "F"
    
    students[roll_no] = {
        "name": student.name,
        "age": student.age,
        "marks": student.marks,
        "subject": student.subject,
        "grade": grade
    }
    save_students(students)
    
    return {
        "message": f"Student {student.name} added successfully",
        "roll_no": roll_no,
        "grade": grade
    }

@app.get("/student/{roll_no}")
def get_student(roll_no: int):
    if roll_no not in students:
        return {"error": "Student not found"}
    return students[roll_no]

@app.get("/all-students")
def get_all_students():
    if not students:
        return {"message": "No students added yet"}
    return students

@app.get("/topper")
def get_topper():
    if not students:
        return {"message": "No students added yet"}
    highest_marks = max(students[r]["marks"] for r in students)
    toppers = {r: students[r] for r in students if students[r]["marks"] == highest_marks}
    return {
        "highest_marks": highest_marks,
        "total_toppers": len(toppers),
        "toppers": toppers
    }

@app.get("/stats")
def get_stats():
    if not students:
        return {"message": "No students added yet"}
    all_marks = [students[r]["marks"] for r in students]
    return {
        "total_students": len(students),
        "average_marks": round(sum(all_marks) / len(all_marks), 2),
        "highest_marks": max(all_marks),
        "lowest_marks": min(all_marks),
        "grade_distribution": {
            "A": len([r for r in students if students[r]["grade"] == "A"]),
            "B": len([r for r in students if students[r]["grade"] == "B"]),
            "C": len([r for r in students if students[r]["grade"] == "C"]),
            "F": len([r for r in students if students[r]["grade"] == "F"]),
        }
    }