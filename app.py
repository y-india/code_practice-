import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="School Records Portal",
    page_icon="🎓",
    layout="centered"
)

# Custom Styling to improve visual appeal
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        height: 3em;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 School Management System")
st.subheader("Centralized Student Manager Website")
st.write("Select an action below to manage school records efficiently.")

st.divider()

# Create a 2x2 grid for the navigation buttons
col1, col2 = st.columns(2)

with col1:
    # Add Student Section


    st.divider()


    if st.button("➕ Add Student", use_container_width=True):
        st.switch_page("pages/add_student.py")
    st.info("Add a new student in school records.")


    st.divider()



    st.write("") # Spacer
    st.divider()

    # Update Student Section
    if st.button("✏️ Update Student Details", use_container_width=True):
        st.switch_page("pages/update_student.py")
    st.info("Edit or modify current student records.")


    st.divider()




st.write("") # Spacer




with col2:
    # View Student Section


    st.divider()



    if st.button("📋 View Student Details", use_container_width=True):
        st.switch_page("pages/view_student.py")
    st.info("Look up and review existing student information.")

    st.divider()




    st.write("") # Spacer
    

    st.divider()

    # Delete Student Section
    if st.button("🗑️ Delete Student", use_container_width=True):
        st.switch_page("pages/delete_student.py")
    st.info("Remove a student from the school records.")

    st.divider()









# section for getting all students 
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 4em;
        font-size: 24px !important;
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)



st.divider()

if st.button("📊 VIEW ALL STUDENT RECORDS (MASTER LIST)", use_container_width=True):
    st.switch_page("pages/get_all_students.py"
    )






st.divider()

# Footer or Quick Stats
st.caption("System Version 1.0.0 | Secure File Access Enabled")

