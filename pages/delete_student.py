import streamlit as st
import requests






API_URL = "http://localhost:8000/students"






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



st.write("") # Spacer
st.write("") # Spacer



if st.button("Back To Home Page", use_container_width=True):
        st.switch_page("app.py")
