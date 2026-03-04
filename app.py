import streamlit as st
import pandas as pd
import time

st.title("Adaptive AI Learning Assistant")

student_id = st.text_input("Enter your Student ID")

if student_id == "":
    st.warning("Please enter your Student ID to continue")
    st.stop()

st.success(f"Welcome {student_id}")

st.header("Learn: Human Heart")

st.write("""
The human heart pumps blood through the body.
The **left ventricle** pumps oxygenated blood to the body.
""")

start_time = time.time()

question = st.radio(
    "Which chamber pumps blood to the body?",
    ["Left Atrium", "Right Ventricle", "Left Ventricle"]
)

if st.button("Submit Answer"):

    end_time = time.time()
    time_taken = round(end_time - start_time, 2)

    score = 1 if question == "Left Ventricle" else 0

    if score == 1:
        st.success("Correct!")
    else:
        st.error("Incorrect!")

    log = pd.DataFrame({
        "student_id": [student_id],
        "topic": ["Heart"],
        "score": [score],
        "time_taken": [time_taken]
    })

    log.to_csv("student_logs.csv", mode="a", header=False, index=False)

    st.write("Your result has been recorded.")