import streamlit as st
import pandas as pd

st.set_page_config(page_title="Teacher Profile Tool", layout="centered")

st.title("Alief ISD Teacher Profile Tool")
st.subheader("Determine your TIA Teacher Type")

# -----------------------------------
# Teacher Info
# -----------------------------------
name = st.text_input("Enter your name")
campus = st.text_input("Enter your campus")

st.markdown("---")

pdf_link = "[View Full TIA Teacher Type Guide](https://aliefisd-my.sharepoint.com/:b:/g/personal/stefan_sanmiguel_aliefisd_net/IQC3HSJ7-pB_Tp_Go-EsT4k0AX7Blc9bpbaJjk_-ZKZ4V4U?e=voJjZK)"

# -----------------------------------
# Campus Type
# -----------------------------------
campus_type = st.radio(
    "What type of campus do you teach at?",
    ["Early Learning Center", "Elementary", "Intermediate", "Middle School", "High School"]
)

# -----------------------------------
# ELC LOGIC
# -----------------------------------
if campus_type == "Early Learning Center":
    pk_self = st.radio(
        "Are you a general education PK Self-Contained teacher?",
        ["Yes", "No"]
    )

else:

    # Grade
    if campus_type == "Elementary":
        grade = st.selectbox("Grade:", ["K","1","2","3","4"])
    elif campus_type == "Intermediate":
        grade = st.selectbox("Grade:", ["5","6"])
    elif campus_type == "Middle School":
        grade = st.selectbox("Grade:", ["7","8"])
    else:
        grade = st.selectbox("Grade:", ["9","10","11","12"])

    # Assignment
    assignment = st.radio(
        "Which best describes your teaching assignment?",
        [
            "Self-Contained General Education",
            "In-Class Support",
            "Dyslexia Teacher",
