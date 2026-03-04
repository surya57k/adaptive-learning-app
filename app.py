import streamlit as st

st.title("Adaptive AI Learning Assistant")

student_id = st.text_input("Enter your Student ID")

if student_id == "":
    st.warning("Please enter your Student ID to continue")
    st.stop()

st.success(f"Welcome {student_id}")

st.header("Welcome Student")

topic = st.selectbox(
    "Choose topic",
    ["Human Heart", "Solar System", "Car Engine"]
)

st.write("You selected:", topic)

question = st.radio(
    "Which chamber pumps blood to the body?",
    ["Left Atrium", "Right Ventricle", "Left Ventricle"]
)

if st.button("Submit"):
    if question == "Left Ventricle":
        st.success("Correct!")
    else:
        st.error("Incorrect")

st.write("This system will later analyze your learning performance.")