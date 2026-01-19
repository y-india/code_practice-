from xml.parsers.expat import model
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os




app = FastAPI()





@app.get("/")
def home():
    return {
        "message": "🎓 Welcome to the School Student Management API 🌟",
        "description": "This API helps schools manage student records easily and securely.",
        "features": {
            "📘 View Students": "Get details of all students or a specific student",
            "➕ Add Student": "Register a new student",
            "✏️ Update Student": "Modify existing student information",
            "🗑️ Delete Student": "Remove a student from the system"
        },
        "status": "✅ API is up and running",
        "made_with": "❤️ FastAPI"
    }




DATA_FILE = r"students.json"

def load_data():
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)





# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)





@app.get("/all_students")
async def view_students():
    data = load_data()
    return data













# Student input model
from pydantic import BaseModel, Field, field_validator, model_validator

class Student(BaseModel):
    name: str # all inputs are required so no ...
    age: int
    class_: int = Field(..., alias="class")
    roll_no: int
    father_name: str
    years_in_school: int

    # Field-level validation
    @field_validator("age")
    @classmethod
    def validate_age(cls, v):
        if not (1 <= v <= 20):
            raise ValueError("Age must be between 1 and 20")
        return v

    @field_validator("class_")
    @classmethod
    def validate_class(cls, v):
        if v != 10:
            raise ValueError("Only class 10 is allowed FOR NOW")
        return v

    @field_validator("name", "father_name", mode="before")
    @classmethod
    def normalize_names(cls, v):
        if not isinstance(v, str):
            return v
        return v.strip().title()

    @property
    def school_id(self):
        return f"{self.class_}{self.roll_no}"
    













# ENDPOINTS 


# models for adding 
from pydantic import BaseModel, Field

class StudentCreate(BaseModel):
    name: str
    age: int
    grade: str
    school_id: str

class StudentOut(BaseModel):
    id: int
    name: str
    age: int
    grade: str
    school_id: str

class CreateStudentResponse(BaseModel):
    message: str
    student: StudentOut



@app.post("/students")
async def add_student(student: Student):
    data = load_data()

    # Check if school_id already exists
    for s in data:
        if s["school_id"] == student.school_id:
            raise HTTPException(
                status_code=400,
                detail="School ID already exists"
            )

    # Generate next ID
    next_id = max((s.get("id", 0) for s in data), default=0) + 1

    new_student = {
        "id": next_id,
        **student.model_dump(by_alias=True),
        "school_id": student.school_id
    }

    data.append(new_student)
    save_data(data)

    return {
        "message": "Student added",
        "id": next_id
    }





# View specific student (GET)
@app.get("/students/{student_id}")
async def view_student(student_id: int):
    data = load_data()
    for s in data:
        if s["id"] == student_id:
            return s
    raise HTTPException(status_code=404, detail="Student not found")






from typing import Optional
from pydantic import BaseModel, Field, field_validator

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    class_: Optional[int] = Field(None, alias="class")
    roll_no: Optional[int] = None
    father_name: Optional[str] = None
    years_in_school: Optional[int] = None

    @field_validator("name", "father_name", mode="before")
    @classmethod
    def normalize_names(cls, v):
        if isinstance(v, str):
            return v.strip().title()
        return v





from fastapi import HTTPException

@app.patch("/students/{student_id}")
async def update_student(student_id: int, student: StudentUpdate):
    data = load_data()
    update_data = student.model_dump(exclude_unset=True, by_alias=True)

    for i, s in enumerate(data):
        if s["id"] == student_id:

            new_record = {**s, **update_data}

            # recompute school_id if needed
            if "class" in update_data or "roll_no" in update_data:
                new_school_id = f"{new_record['class']}{new_record['roll_no']}"

                if any(
                    other["school_id"] == new_school_id
                    and other["id"] != student_id
                    for other in data
                ):
                    raise HTTPException(
                        status_code=409,
                        detail="School ID already exists"
                    )

                new_record["school_id"] = new_school_id

            data[i] = new_record
            save_data(data)

            return {"message": "Student updated"}

    raise HTTPException(status_code=404, detail="Student not found")




# Delete student (DELETE)
@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    data = load_data()
    for i, s in enumerate(data):
        if s["id"] == student_id:
            del data[i]
            save_data(data)
            return {"message": "Student deleted"}
    raise HTTPException(status_code=404, detail="Student not found")








 















