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

    # Computed / transformed output
    @model_validator(mode="after")
    def normalize_and_compute(self):
        self.name = self.name.upper()
        return self

    @property
    def school_id(self):
        return f"{self.class_}{self.roll_no}"
    













# ENDPOINTS 


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
# model for partial update
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    class_: Optional[int] = None
    roll_no: Optional[int] = None
    father_name: Optional[str] = None
    years_in_school: Optional[int] = None
    school_id: Optional[str] = None

    @model_validator(mode="after")
    def compute_school_id(self):
        if self.class_ is not None and self.roll_no is not None:
            self.school_id = f"{self.class_}{self.roll_no}"
        return self








# Update student (PUT)
from fastapi import HTTPException

@app.put("/students/{student_id}")
async def update_student(student_id: int, student: StudentUpdate):
    data = load_data()
    update_data = student.model_dump(exclude_unset=True)

    for i, s in enumerate(data):
        if s["id"] == student_id:

            if "school_id" in update_data:
                if any(
                    other["school_id"] == update_data["school_id"]
                    and other["id"] != student_id
                    for other in data
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="School ID already exists"
                    )

            data[i] = {**s, **update_data}
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
























