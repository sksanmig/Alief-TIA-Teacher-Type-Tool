import streamlit as st
import pandas as pd

# ✅ Use wide so banner spans properly
st.set_page_config(page_title="Teacher Profile Tool", layout="wide")

# -----------------------------------
# ✅ GREEN BANNER (SAFE METHOD)
# -----------------------------------
st.markdown(
    """
    <style>
    .banner {
        background-color: #008066;
        padding: 15px;
        margin-bottom: 20px;
    }
    .banner-content {
        display: flex;
        align-items: center;
        max-width: 900px;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="banner">
        <div class="banner-content">
            <img src="https://cmsv2-assets.apptegy.net/uploads/20164/file/3279863/11ac19c0-01c6-4b6f-8e31-78f316d1613d.png"
                 style="height:60px; margin-right:20px;">
            <div>
                <div style="color:white; font-size:24px; font-weight:bold;">
                    Alief ISD Teacher Profile Tool
                </div>
                <div style="color:white;">
                    Determine your TIA Teacher Type
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ✅ Switch back to centered content below banner
st.markdown("<div style='max-width:800px; margin:auto;'>", unsafe_allow_html=True)

# -----------------------------------
# ✅ STYLING
# -----------------------------------
st.markdown("""
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
    border: 2px solid #008066 !important08066;
    padding: 8px;
    border-radius: 6px;
}
.stMultiSelect > div {
    border: 2px solid #008066;
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

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
    pk_self = st.radio("Are you a PK Self-Contained teacher?", ["Yes","No"])

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
    if campus_type == "High School" and assignment in ["Science","RLA / Reading","Social Studies"]:
        teaches_eoc = st.radio(
            "Teach EOC course?",
            ["Biology","English I","English II","U.S. History","None"]
        )

# -----------------------------------
# ✅ RESULT LOGIC
# -----------------------------------
if st.button("Show My Result"):

    if not name or not campus:
        st.error("Please complete required fields.")
    else:
        result_type = "Unknown"

        if campus_type == "Early Learning Center":
            result_type = "1" if pk_self == "Yes" else "12"

        else:
            if assignment == "Self-Contained General Education":
                if any(g in ["3","4","5"] for g in grades):
                    result_type = "5"
                elif any(g in ["K","1","2"] for g in grades):
                    result_type = "2"

            elif teaches_algebra1 == "Yes":
                result_type = "8"

            elif assignment == "Science":
                result_type = "8" if ("5" in grades or "8" in grades) else "9"

            elif assignment == "Social Studies":
                result_type = "8" if "8" in grades else "9"

            elif teaches_eoc and teaches_eoc != "None":
                result_type = "8"

            elif assignment == "Math" and any(g in ["3","4","5","6","7","8"] for g in grades):
                result_type = "6"

            elif assignment == "RLA / Reading" and any(g in ["3","4","5","6","7","8"] for g in grades):
                result_type = "7"

            elif campus_type == "High School":
                result_type = "9"

            elif assignment == "PE":
                result_type = "10"

            elif assignment == "Special Education / Specialized Program":
                result_type = "12"

            else:
                result_type = "11"

        # ✅ Display
        st.success(f"You are TIA Teacher Type {result_type}")
