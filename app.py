import streamlit as st
import pandas as pd

# ✅ Keep layout clean and centered
st.set_page_config(page_title="Teacher Profile Tool", layout="centered")

# -----------------------------------
# ✅ FINAL WORKING BANNER (WHITE BOX)
# -----------------------------------
st.markdown(
    """
    <div style="background-color:#008066; padding:15px; margin-bottom:20px; border-radius:6px;">
        <div style="display:flex; align-items:center;">

            <div style="background-color:white; padding:8px 16px; border-radius:6px; margin-right:20px;">
                <img src="https://cmsv2-assets.apptegy.net/uploads/20164/logo/22855/AliefSmartChoice.png" style="height:45px;">
            </div>

            <div>
                <div style="color:white; font-size:22px; font-weight:bold;">
                    Alief ISD Teacher Profile Tool
                </div>
                <div style="color:white; font-size:14px;">
                    Determine your TIA Teacher Type
                </div>
            </div>

        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# ✅ CLEAN STYLING
# -----------------------------------
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #008066;
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }

    .stButton > button:hover {
        background-color: #006655;
    }

    .stTextInput input {
        border: 2px solid #008066 !important;
        border-radius: 6px;
    }

    .stRadio > div {
        border: 2px solid #008066;
        padding: 8px;
        border-radius: 6px;
    }

    .stMultiSelect > div {
        border: 2px solid #008066;
        border-radius: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# ✅ INPUTS
# -----------------------------------
name = st.text_input("Enter your name")
campus = st.text_input("Enter your campus")

st.markdown("---")

campus_type = st.radio(
    "What type of campus do you teach at?",
    ["Early Learning Center", "Elementary", "Intermediate", "Middle School", "High School"]
)

# -----------------------------------
# ✅ ELC
# -----------------------------------
if campus_type == "Early Learning Center":
    pk_self = st.radio("Are you a PK Self-Contained teacher?", ["Yes", "No"])

else:

    if campus_type == "Elementary":
        grades = st.multiselect("Grades:", ["K","1","2","3","4","5"])
    elif campus_type == "Intermediate":
        grades = st.multiselect("Grades:", ["5","6"])
    elif campus_type == "Middle School":
        grades = st.multiselect("Grades:", ["6","7","8"])
    else:
        grades = st.multiselect("Grades:", ["9","10","11","12"])

    assignment = st.radio(
        "Assignment",
        [
            "Self-Contained General Education",
            "Math",
            "RLA / Reading",
            "Science",
            "Social Studies",
            "PE",
            "Special Education / Specialized Program"
        ]
    )

    teaches_algebra1 = None
    if assignment == "Math" and campus_type in ["Middle School","High School"]:
        teaches_algebra1 = st.radio("Teach Algebra I?", ["Yes","No"])

    teaches_eoc = None
