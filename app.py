import streamlit as st
import pandas as pd

st.set_page_config(page_title="Teacher Profile Tool", layout="wide")

# -----------------------------------
# ✅ SAFE HEADER (NO HTML BUGS)
# -----------------------------------
st.image(
    "https://cmsv2-assets.apptegy.net/uploads/20164/logo/22855/AliefSmartChoice.png",
    width=200
)

st.markdown("<h2 style='color:#008066;'>Alief ISD Teacher Profile Tool</h2>", unsafe_allow_html=True)
st.markdown("Determine your TIA Teacher Type")

st.markdown("---")

# -----------------------------------
# ✅ STYLING
# -----------------------------------
st.markdown("""
<style>
.stButton>button {
    background-color: #008066;
    color: white;
    font-weight: bold;
    border-radius: 8px;
}
.stTextInput input {
    border: 2px solid #008066 !important;
}
.stRadio > div {
    border: 2px solid #008066;
    padding: 8px;
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
    if assignment == "Math" and campus_type in ["Middle School", "High School"]:
        teaches_algebra1 = st.radio("Teach Algebra I?", ["Yes", "No"])

    teaches_eoc = None
    if campus_type == "High School" and assignment in ["Science", "RLA / Reading", "Social Studies"]:
        teaches_eoc = st.radio(
            "Teach EOC course?",
            ["Biology", "English I", "English II", "U.S. History", "None"]
        )

# -----------------------------------
# ✅ RESULT
# -----------------------------------
if st.button("Show My Result"):

    if not name or not campus:
        st.error("Please complete required fields.")
    else:

        result_type = "Unknown"

        if campus_type == "Early Learning Center":
            result_type = "1" if pk_self == "Yes" else "12"

        else:

            # ✅ SELF-CONTAINED
            if assignment == "Self-Contained General Education":
                if any(g in ["3","4","5"] for g in grades):
                    result_type = "5"
                elif any(g in ["K","1","2"] for g in grades):
                    result_type = "2"

            # ✅ TYPE 8
            elif teaches_algebra1 == "Yes":
                result_type = "8"

            elif assignment == "Science":
                if "5" in grades or "8" in grades:
                    result_type = "8"
                else:
                    result_type = "9"

            elif assignment == "Social Studies":
                if "8" in grades:
                    result_type = "8"
                else:
                    result_type = "9"

            elif teaches_eoc is not None and teaches_eoc != "None":
                result_type = "8"

            # ✅ TYPE 6
            elif assignment == "Math" and any(g in ["3","4","5","6","7","8"] for g in grades):
                result_type = "6"

            # ✅ TYPE 7
            elif assignment == "RLA / Reading" and any(g in ["3","4","5","6","7","8"] for g in grades):
                result_type = "7"

            # ✅ HIGH SCHOOL NON-EOC
            elif campus_type == "High School":
                result_type = "9"

            elif assignment == "PE":
                result_type = "10"

            elif assignment == "Special Education / Specialized Program":
                result_type = "12"

            else:
                result_type = "11"

        # -----------------------------------
        # ✅ DESCRIPTIONS
        # -----------------------------------
        descriptions = {
            "1": "PK Self-Contained General Education Teachers.",
            "2": "K-2 Self-Contained (SC) General Education Teachers and In-Class Support Teachers.",
            "5": "3-5 Self-Contained General Education Teachers and In-Class Support Teachers. This type includes a student perception survey.",
            "6": "3-8 Math, Math/Science General Education Teachers. This type includes a student perception survey.",
            "7": "3-8 RLA General Education Teachers. This type includes a student perception survey.",
            "8": "STAAR-tested teachers including 5th/8th Science, 8th Social Studies, and HS EOC courses.",
            "9": "3-12 TEKSReady Teachers of non-STAAR courses.",
            "10": "K-12 Physical Education Teachers.",
            "11": "SLO-based elective teachers.",
            "12": "Special program teachers."
        }

        # ✅ ASSESSMENTS
        assessments = {
            "1": "Circle",
            "2": "Amplify mClass-RLA, iReady-Math",
            "5": "iReady-Math, iReady-Reading, STAAR VAM",
            "6": "iReady Math, STAAR VAM",
            "7": "iReady Reading, STAAR VAM",
            "8": "SLOs, STAAR VAM",
            "9": "TEKSReady Pre/Post-Test, SLO",
            "10": "FitnessGram, SLO",
            "11": "SLO",
            "12": "SLO"
        }

        if result_type in ["5","6","7","8","9","10","11"]:
            survey = "This teacher type does include a student perception survey for students in grades 3–12."
        else:
            survey = "This teacher type does not include a student perception survey."

        # ✅ DISPLAY
        st.success(f"You are TIA Teacher Type {result_type}")

        st.markdown("### Description")
        st.info(descriptions.get(result_type, ""))

        st.markdown("### TIA Assessments")
        st.info(assessments.get(result_type, ""))

        st.markdown("### Student Perception Survey")
        st.info(survey)
