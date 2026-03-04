import streamlit as st
import pandas as pd
import time
import plotly.express as px
from sklearn.cluster import KMeans

st.title("Adaptive AI Learning Assistant")

USER_FILE = "users.csv"
LOG_FILE = "student_logs.csv"

# -------------------------
# Create files if not exist
# -------------------------

try:
    pd.read_csv(USER_FILE)
except:
    pd.DataFrame(columns=["rollno","password"]).to_csv(USER_FILE,index=False)

try:
    pd.read_csv(LOG_FILE)
except:
    pd.DataFrame(columns=["student_id","topic","score","time_taken"]).to_csv(LOG_FILE,index=False)

# -------------------------
# MAIN MENU
# -------------------------

menu = st.sidebar.selectbox(
    "Menu",
    ["Login","Register","Teacher Login"]
)

# -------------------------
# REGISTER
# -------------------------

if menu == "Register":

    st.header("Student Registration")

    rollno = st.text_input("Roll Number / Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):

        users = pd.read_csv(USER_FILE)

        if rollno in users["rollno"].values:
            st.error("User already exists")

        else:

            new_user = pd.DataFrame({
                "rollno":[rollno],
                "password":[password]
            })

            users = pd.concat([users,new_user])
            users.to_csv(USER_FILE,index=False)

            st.success("Registration successful. Please login.")

# -------------------------
# STUDENT LOGIN
# -------------------------

elif menu == "Login":

    st.header("Student Login")

    rollno = st.text_input("Roll Number / Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        users = pd.read_csv(USER_FILE)

        user = users[
            (users["rollno"]==rollno) &
            (users["password"]==password)
        ]

        if not user.empty:

            st.session_state["user"] = rollno
            st.success("Login successful")

        else:
            st.error("Invalid login")

# -------------------------
# TEACHER LOGIN
# -------------------------

elif menu == "Teacher Login":

    st.header("Teacher Login")

    username = st.text_input("Teacher Username")
    password = st.text_input("Teacher Password", type="password")

    if st.button("Login as Teacher"):

        if username == "admin" and password == "admin123":
            st.session_state["teacher"] = True
            st.success("Teacher login successful")
        else:
            st.error("Invalid teacher credentials")

# -------------------------
# STUDENT PANEL
# -------------------------

if "user" in st.session_state:

    student_id = st.session_state["user"]

    st.sidebar.success(f"Logged in as {student_id}")

    page = st.sidebar.selectbox(
        "Navigation",
        ["Learn & Quiz","My Analytics","AI Assessment","Logout"]
    )

    # -------------------------
    # LEARN & QUIZ
    # -------------------------

    if page == "Learn & Quiz":

        topic = st.selectbox(
            "Choose Topic",
            ["Human Heart","Solar System"]
        )

        if topic == "Human Heart":

            st.header("Human Heart")

            st.write("""
            The heart pumps oxygenated blood through the body.
            The **left ventricle** sends blood to the entire body.
            """)

            question = st.radio(
                "Which chamber pumps blood to the body?",
                ["Left Atrium","Right Ventricle","Left Ventricle"]
            )

            correct_answer = "Left Ventricle"

        elif topic == "Solar System":

            st.header("Solar System")

            st.write("""
            The Sun is the center of the solar system.
            Planets revolve around the Sun.
            """)

            question = st.radio(
                "Which planet is called the Red Planet?",
                ["Earth","Mars","Venus"]
            )

            correct_answer = "Mars"

        if "start_time" not in st.session_state:
            st.session_state.start_time = time.time()

        if st.button("Submit Answer"):

            end_time = time.time()
            time_taken = round(end_time - st.session_state.start_time,2)

            score = 1 if question == correct_answer else 0

            if score:
                st.success("Correct!")
            else:
                st.error("Incorrect")

            log = pd.DataFrame({
                "student_id":[student_id],
                "topic":[topic],
                "score":[score],
                "time_taken":[time_taken]
            })

            log.to_csv(LOG_FILE,mode="a",header=False,index=False)

            st.write(f"Time taken: {time_taken} seconds")

            st.session_state.start_time = time.time()

    # -------------------------
    # STUDENT ANALYTICS
    # -------------------------

    elif page == "My Analytics":

        st.header("Your Learning Analytics")

        try:

            df = pd.read_csv(LOG_FILE)

            student_df = df[df["student_id"] == student_id]

            st.dataframe(student_df)

            avg_scores = student_df.groupby("topic")["score"].mean().reset_index()

            fig = px.bar(
                avg_scores,
                x="topic",
                y="score",
                title="Your Average Score"
            )

            st.plotly_chart(fig)

            fig2 = px.histogram(
                student_df,
                x="time_taken",
                title="Your Response Time"
            )

            st.plotly_chart(fig2)

        except:
            st.info("No learning data yet.")

    # -------------------------
    # AI ASSESSMENT
    # -------------------------

    elif page == "AI Assessment":

        st.header("AI Learning Assessment")

        try:

            df = pd.read_csv(LOG_FILE)

            student_df = df[df["student_id"] == student_id]

            if len(student_df) >= 3:

                X = student_df[["score","time_taken"]]

                kmeans = KMeans(n_clusters=3,random_state=0)

                student_df["cluster"] = kmeans.fit_predict(X)

                labels = {
                    0:"Fast Learner",
                    1:"Careful Learner",
                    2:"Needs Reinforcement"
                }

                student_df["learner"] = student_df["cluster"].map(labels)

                learner = student_df.iloc[-1]["learner"]

                st.write(f"Your Learning Type: **{learner}**")

                if learner == "Fast Learner":
                    st.success("You understand concepts quickly.")

                elif learner == "Careful Learner":
                    st.info("You learn carefully. Review once more.")

                else:

                    st.warning("You may need reinforcement.")

                    st.write("""
                    Extra Explanation

                    The left ventricle pumps oxygenated blood
                    through the aorta to the entire body.
                    """)

            else:
                st.info("Complete more quizzes for AI assessment.")

        except:
            st.info("No learning data yet.")

    # -------------------------
    # LOGOUT
    # -------------------------

    elif page == "Logout":

        st.session_state.clear()
        st.success("Logged out successfully")
        st.stop()

# -------------------------
# TEACHER DASHBOARD
# -------------------------

if "teacher" in st.session_state:

    st.header("Teacher Dashboard")

    try:

        df = pd.read_csv(LOG_FILE)

        st.subheader("All Student Records")
        st.dataframe(df)

        st.subheader("Class Performance by Topic")

        topic_scores = df.groupby("topic")["score"].mean().reset_index()

        fig = px.bar(
            topic_scores,
            x="topic",
            y="score",
            title="Average Score per Topic"
        )

        st.plotly_chart(fig)

        st.subheader("Student Performance")

        student_scores = df.groupby("student_id")["score"].mean().reset_index()

        fig2 = px.bar(
            student_scores,
            x="student_id",
            y="score",
            title="Average Score per Student"
        )

        st.plotly_chart(fig2)

        st.subheader("Response Time Distribution")

        fig3 = px.histogram(
            df,
            x="time_taken",
            title="Student Response Time Distribution"
        )

        st.plotly_chart(fig3)

    except:
        st.info("No student data yet.")