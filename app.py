import streamlit as st
import pandas as pd
import time
import plotly.express as px

st.title("Adaptive AI Learning Assistant")

# -------------------------
# Student Login
# -------------------------

student_id = st.text_input("Enter your Student ID")

if student_id == "":
    st.warning("Please enter your Student ID to continue")
    st.stop()

st.success(f"Welcome {student_id}")

# -------------------------
# Learning Section
# -------------------------

st.header("Learn: Human Heart")

st.write("""
The human heart pumps blood through the body.
The **left ventricle** pumps oxygenated blood to the body.
""")

# Start timer only once
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# Quiz Question
question = st.radio(
    "Which chamber pumps blood to the body?",
    ["Left Atrium", "Right Ventricle", "Left Ventricle"]
)

# Submit Button
if st.button("Submit Answer"):

    end_time = time.time()
    time_taken = round(end_time - st.session_state.start_time, 2)

    score = 1 if question == "Left Ventricle" else 0

    if score == 1:
        st.success("Correct!")
    else:
        st.error("Incorrect!")

    st.write(f"Time taken: {time_taken} seconds")

    # Save student result
    log = pd.DataFrame({
        "student_id": [student_id],
        "topic": ["Heart"],
        "score": [score],
        "time_taken": [time_taken]
    })

    log.to_csv("student_logs.csv", mode="a", header=False, index=False)

    st.write("Your result has been recorded.")

    # Reset timer for next question
    st.session_state.start_time = time.time()

# -------------------------
# Learning Analytics
# -------------------------

st.header("Learning Analytics")

try:
    df = pd.read_csv(
        "student_logs.csv",
        names=["student_id", "topic", "score", "time_taken"]
    )

    st.write("### Raw Student Data")
    st.dataframe(df)

    st.write("### Average Score per Topic")

    avg_scores = df.groupby("topic")["score"].mean().reset_index()

    fig = px.bar(
        avg_scores,
        x="topic",
        y="score",
        title="Average Student Score by Topic"
    )

    st.plotly_chart(fig)

    st.write("### Response Time Distribution")

    fig2 = px.histogram(
        df,
        x="time_taken",
        title="Response Time Distribution"
    )

    st.plotly_chart(fig2)

except:
    st.info("No student data recorded yet.")
# -------------------------
# AI Learner Classification
# -------------------------

st.header("AI Learning Assessment")

try:
    df = pd.read_csv(
        "student_logs.csv",
        names=["student_id", "topic", "score", "time_taken"]
    )

    from sklearn.cluster import KMeans

    # Features used for clustering
    X = df[["score", "time_taken"]]

    # Train simple clustering model
    kmeans = KMeans(n_clusters=3, random_state=0)
    df["learner_type"] = kmeans.fit_predict(X)

    # Map cluster numbers to labels
    learner_labels = {
        0: "Fast Learner",
        1: "Careful Learner",
        2: "Needs Reinforcement"
    }

    df["learner_label"] = df["learner_type"].map(learner_labels)

    st.write("### AI Learner Classification")
    st.dataframe(df[["student_id", "score", "time_taken", "learner_label"]])

except:
    st.info("Not enough data for AI analysis yet.")
# -------------------------
# Adaptive Learning Engine
# -------------------------

st.header("Adaptive Learning Recommendation")

try:
    df = pd.read_csv(
        "student_logs.csv",
        names=["student_id", "topic", "score", "time_taken"]
    )

    from sklearn.cluster import KMeans

    X = df[["score", "time_taken"]]

    kmeans = KMeans(n_clusters=3, random_state=0)
    df["learner_type"] = kmeans.fit_predict(X)

    learner_labels = {
        0: "Fast Learner",
        1: "Careful Learner",
        2: "Needs Reinforcement"
    }

    df["learner_label"] = df["learner_type"].map(learner_labels)

    # get current student latest result
    student_data = df[df["student_id"] == student_id].iloc[-1]

    learner = student_data["learner_label"]

    st.write(f"### Your Learning Type: {learner}")

    if learner == "Fast Learner":
        st.success("You understand quickly! You can move to advanced topics.")

    elif learner == "Careful Learner":
        st.info("You learn carefully. Review the concept once more for mastery.")

    else:
        st.warning("You may need reinforcement. Let's review the concept again.")

        st.write("### Extra Explanation")

        st.write("""
        The **left ventricle** is the strongest chamber of the heart.
        It pumps oxygen-rich blood through the aorta to the rest of the body.
        """)

except:
    st.info("Complete the quiz to receive adaptive recommendations.")