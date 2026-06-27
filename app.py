import streamlit as st
import pandas as pd

# ✅ Centered layout
st.set_page_config(page_title="Teacher Profile Tool", layout="centered")

# -----------------------------------
# ✅ CLEAN HEADER (NO HTML ISSUES)
# -----------------------------------
col1, col2 = st.columns([1, 4])

with col1:
    st.image(
        "https://cmsv2-assets.apptegy.net/uploads/20164/logo/22855/AliefSmartChoice.png",
        width=110
    )

with col2:
    st.markdown("### **Alief ISD Teacher Profile Tool**")
    st.markdown("Determine your TIA Teacher Type")

st.markdown("---")

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
    if assignment == "Math" and campus_type in ["Middle School","High School"]:
        teaches_algebra1 = st.radio("Teach Algebra I?", ["Yes","No"])

    teaches_eoc = None
    if campus_type == "High School" and assignment in ["Science","RLA / Reading","Social Studies"]:
        teaches_eoc = st.radio(
            "Teach EOC course?",
            ["Biology","English I","English II","U.S. History","None"]
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
            # Self-contained logic
            if assignment == "Self-Contained General Education":
                if any(g in ["3","4","5"] for g in grades):
                    result_type = "5"
                elif any(g in ["K","1","2"] for g in grades):
                    result_type = "2"

            # STAAR priority
            elif teaches_algebra1 == "Yes":
                result_type = "8"

            elif assignment == "Science":
                result_type = "8" if ("5" in grades or "8" in grades) else "9"

            elif assignment == "Social Studies":
                result_type = "8" if "8" in grades else "9"

            elif teaches_eoc is not None and teaches_eoc != "None":
                result_type = "8"

            # Math / RLA
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

        # -----------------------------------
        # ✅ DESCRIPTIONS (FULL)
        # -----------------------------------
        descriptions = {
            "1": "PK Self-Contained General Education Teachers.",
            "2": "K-2 Self-Contained (SC) General Education Teachers and In-Class Support Teachers.",
            "3": "K-2 Math, Math/Science General Education Teachers and In-Class Support Teachers.",
            "4": "K-2 RLA, RLA/Social Studies General Education Teachers, In-Class Support Teachers, and Dyslexia Teachers.",
            "5": "3-5 Self-Contained General Education Teachers and In-Class Support Teachers. This type includes a student perception survey.",
            "6": "3-8 Math, Math/Science General Education Teachers and In-Class Support Teachers. This type includes a student perception survey.",
            "7": "3-8 RLA, RLA/Social Studies General Education Teachers, In-Class Support Teachers, Dyslexia Teachers, and ELD Interventionist. This type includes a student perception survey.",
            "8": "5-8 STAAR Science and STAAR Social Studies Teachers, 9-12 STAAR EOC teachers, In-Class Support Teachers, and general Interventionist. This type includes a student perception survey.",
            "9": "3-12 TEKSReady general education and In-Class Support Teachers of non-STAAR core, Elective, or Block Courses. This type includes a student perception survey.",
            "10": "K-12 Physical Education Teachers. This type includes a student perception survey.",
            "11": "3-12 SLO Block and Elective General Education Teachers. This type includes a student perception survey.",
            "12": "Other PK-12 Special Education Teachers (Life, Reach, Read 180), ALC Teachers, ESCE Teachers, or Block ELC Teachers."
        }

        # -----------------------------------
        # ✅ ASSESSMENTS (FIXED)
        # -----------------------------------
        assessments = {
            "1": "Circle",
            "2": "Amplify mClass-RLA, iReady-Math",
            "3": "iReady-Math, STEMScopes",
            "4": "iReady-Reading, Amplify mClass-RLA",
            "5": "iReady-Math, iReady-Reading, STAAR VAM",
            "6": "iReady-Math, Teacher STAAR VAM",
            "7": "iReady Reading, Teacher STAAR VAM",
            "8": "SLOs, Teacher STAAR VAM",
            "9": "SLO, TEKSReady Pre/Post-Test",
            "10": "SLO, FitnessGram",
            "11": "SLO",
            "12": "SLO"
        }

        # -----------------------------------
        # ✅ SURVEY
        # -----------------------------------
        survey = (
            "This teacher type DOES include a student perception survey for grades 3–12."
            if result_type in ["5","6","7","8","9","10","11"]
            else "This teacher type does NOT include a student perception survey."
        )

        # -----------------------------------
        # ✅ DISPLAY
        # -----------------------------------
        st.success(f"You are TIA Teacher Type {result_type}")

        st.markdown("### Description")
        st.info(descriptions.get(result_type))

        st.markdown("### TIA Assessments")
        st.info(assessments.get(result_type))

        st.markdown("### Student Perception Survey")
        st.info(survey)
