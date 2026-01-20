import streamlit as st
import requests

st.title("📋 View All Students")

# Define your FastAPI URL
API_URL = "http://127.0.0.1:8000/all_students"

# Logic to fetch data
res = requests.get(API_URL)

if res.status_code == 200:
    data = res.json()
    if data:
        # Displaying the list as a simple, clean table
        st.table(data)
        st.success(f"Successfully loaded {len(data)} records")
    else:
        st.warning("No students found in the database")

elif res.status_code == 404:
    st.error("Records not found")

else:
    st.error("Failed to connect to the server")

# Back button for easy navigation
if st.button("Back to Home"):
    st.switch_page("app.py")