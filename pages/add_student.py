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


st.write("") # Spacer
st.write("") # Spacer



if st.button("Back To Home Page", use_container_width=True):
        st.switch_page("app.py")
