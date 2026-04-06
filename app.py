import streamlit as st
import requests

API = "https://student-tracker-api-ql07.onrender.com"

st.title("Student Project Tracker")
st.caption("Submit projects, view them, and predict their category using AI")

# --- SESSION STATE (keeps token alive across interactions) ---
if "token" not in st.session_state:
    st.session_state.token = None

# --- LOGIN ---
st.header("Login")
col1, col2 = st.columns(2)
with col1:
    username = st.text_input("Username")
with col2:
    password = st.text_input("Password", type="password")

if st.button("Login"):
    res = requests.post(f"{API}/login", data={
        "username": username,
        "password": password
    })
    if res.status_code == 200:
        st.session_state.token = res.json()["access_token"]
        st.success("Logged in successfully.")
    else:
        st.error("Invalid username or password.")

# --- SUBMIT PROJECT ---
st.divider()
st.header("Submit a Project")

title       = st.text_input("Project title")
description = st.text_area("Project description")
status      = st.selectbox("Status", ["pending", "in progress", "completed"])

if st.button("Submit Project"):
    if not st.session_state.token:
        st.error("Please login first.")
    elif not title or not description:
        st.error("Title and description are required.")
    else:
        res = requests.post(
            f"{API}/projects",
            json={"title": title, "description": description, "status": status},
            headers={"Authorization": f"Bearer {st.session_state.token}"}
        )
        if res.status_code == 201:
            st.success(f"Project '{res.json()['title']}' created successfully.")
        else:
            st.error("Failed to create project.")

# --- VIEW PROJECTS ---
st.divider()
st.header("All Projects")

if st.button("Load Projects"):
    if not st.session_state.token:
        st.error("Please login first.")
    else:
        res = requests.get(
            f"{API}/projects",
            headers={"Authorization": f"Bearer {st.session_state.token}"}
        )
        if res.status_code == 200:
            projects = res.json()
            if not projects:
                st.info("No projects yet.")
            else:
                for p in projects:
                    with st.container(border=True):
                        st.subheader(p["title"])
                        st.write(p["description"])
                        col1, col2 = st.columns(2)
                        with col1:
                            st.caption(f"Status: {p['status']}")
                        with col2:
                            st.caption(f"Created: {p['created_at'].split('T')[0]}")
        else:
            st.error("Failed to load projects.")

# --- AI PREDICTOR ---
st.divider()
st.header("AI Category Predictor")

predict_input = st.text_input("Describe your project")

if st.button("Predict Category"):
    if not predict_input:
        st.error("Please enter a description.")
    else:
        res = requests.post(
            f"{API}/predict",
            json={"description": predict_input}
        )
        if res.status_code == 200:
            data = res.json()
            st.success(f"Predicted category: **{data['category']}**")
            st.caption(f"Description: {data['description']}")
        else:
            st.error("Prediction failed.")
