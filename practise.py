import json
import os




DATA_FILE = r"C:\Users\User\OneDrive\Desktop\fastapi\students.json"

def load_data():
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

print(load_data() )




from pydantic import BaseModel, Field

class Student(BaseModel):
    school_id: str = Field(..., alias="school id")

    class Config:
        populate_by_name = True






print("\n\n\n\n")
for item in load_data():
    data = Student(**item)
    print(data.school_id)

print("\n\n\n\n")






input_school_id = int(input("Enter school_id to search: "))  



print("Searching for school_id:", input_school_id)




for data in load_data():
    if input_school_id == data["school_id"]:
        print("Found:", data)
        break
else:
    print("Not Found")
