import requests
import streamlit as st






API_URL = "http://localhost:8000/students"










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

st.write("") # Spacer
st.write("") # Spacer



if st.button("Back To Home Page", use_container_width=True):
        st.switch_page("app.py")
