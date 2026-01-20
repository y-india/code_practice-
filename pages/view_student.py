import requests
import streamlit as st

API_URL = "http://localhost:8000/students"



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


st.write("") # Spacer
st.write("") # Spacer



if st.button("Back To Home Page", use_container_width=True):
        st.switch_page("app.py")
