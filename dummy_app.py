import requests
import streamlit as st

API_URL = "http://localhost:8000/students"

st.title("Add Student")

name = st.text_input("Name")
age = st.number_input("Age", min_value=15, max_value=20)
class_value = st.number_input("Class", min_value=10, max_value=10, step=1) # for now only class 10 is allowed
roll_no = st.number_input("Roll Number", min_value=1)
father_name = st.text_input("Father Name")
years_in_school = st.number_input("Years in School", min_value=0 , max_value=10)

if st.button("Submit"):
    payload = {
        "name": name,
        "age": age,
        "class": class_value,
        "roll_no": roll_no,
        "father_name": father_name,
        "years_in_school": years_in_school
    }

    res = requests.post(API_URL, json=payload)

    if res.status_code == 200:
        st.success(f"Student added with ID {res.json()['id']}")
    elif res.status_code == 400:
        st.error(res.json().get("detail", "Validation error"))
    else:
        st.error("Unexpected error")





# writing for get a specific student 
st.divider()
st.title("View Student")

student_id = st.number_input("Student ID", min_value=1, step=1)

if st.button("Fetch Student"):
    res = requests.get(f"{API_URL}/{student_id}")

    if res.status_code == 200:
        student = res.json()
        st.subheader("Student Details")
        st.json(student)
    elif res.status_code == 404:
        st.error("Student not found")
    else:
        st.error("Unexpected error")




# now update ui 
st.divider()
st.title("Update Student")

update_id = st.number_input("Student ID to Update", min_value=1, step=1)

new_name = st.text_input("New Name")
new_age = st.number_input("New Age", min_value=0, max_value=20)
new_roll = st.number_input("New Roll Number", min_value=0)
new_father = st.text_input("New Father Name")
new_years = st.number_input("New Years in School", min_value=0, max_value=10)

if st.button("Update"):
    payload = {}

    if new_name:
        payload["name"] = new_name
    if new_age > 0:
        payload["age"] = new_age
    if new_roll > 0:
        payload["roll_no"] = new_roll
    if new_father:
        payload["father_name"] = new_father
    if new_years > 0:
        payload["years_in_school"] = new_years

    res = requests.patch(f"{API_URL}/{update_id}", json=payload)

    if res.status_code == 200:
        st.success("Student updated")
    elif res.status_code == 404:
        st.error("Student not found")
    elif res.status_code == 409:
        st.error("School ID conflict")
    else:
        st.error("Unexpected error")


st.divider()
st.title("Delete Student")

delete_id = st.number_input(
    "Student ID",
    min_value=1,
    step=1,
    key="delete_id"
)

confirm = st.checkbox("Confirm deletion")

if st.button("Delete"):
    if not confirm:
        st.warning("Please confirm deletion")
    else:
        res = requests.delete(f"{API_URL}/{delete_id}")

        if res.status_code == 200:
            st.success(res.json().get("message", "Student deleted"))
        elif res.status_code == 404:
            st.error("Student not found")
        else:
            st.error("Unexpected error")
