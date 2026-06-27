import streamlit as st
import pandas as pd

st.set_page_config(page_title="Teacher Profile Tool", layout="centered")

# -----------------------------------
# ✅ FIXED BANNER HEADER (NO ERRORS)
# -----------------------------------
st.markdown(
    """
    <div style="
        background-color: #008066;
        padding: 15px;
        border-radius: 8px;
        display: flex;
        align-items: center;">
        
        <img src="https://cmsv2-assets.apptegy.net/uploads/20164/logo/22855/AliefSmartChoice.png"
             style="height:60px; margin-right:20px;">
             
        <div>
            <h2 style="color:white; margin:0;">
                Alief ISD Teacher Profile Tool
            </h2>
            <p style="color:white; margin:0;">
                Determine your TIA Teacher Type
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# -----------------------------------
# ✅ CUSTOM STYLING
# -----------------------------------
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #008066;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #006655;
    }

    .stTextInput input {
        border: 2px solid #008066;
        border-radius: 6px;
    }

    .stRadio > div {
        border: 2px solid #008066;
        padding: 10px;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# LINK
# -----------------------------------
pdf_link = "[View Full TIA Teacher Type Guide](https://aliefisd-my.sharepoint.com/:b:/g/personal/stefan_sanmiguel_aliefisd_net/IQC3HSJ7-pB_Tp_Go-EsT4k0AX7Blc9bpbaJjk_-ZKZ4V4U?e=voJjZK)"

# -----------------------------------
# TEACHER INFO
# -----------------------------------
name = st.text_input("Enter your name")
campus = st.text_input("Enter your campus")

st.markdown("---")

# -----------------------------------
# CAMPUS TYPE
# -----------------------------------
campus_type = st.radio(
    "What type of campus do you teach at?",
    ["Early Learning Center", "Elementary", "Intermediate", "Middle School", "High School"]
)

# -----------------------------------
# ELC
# -----------------------------------
if campus_type == "Early Learning Center":
    pk_self = st.radio("Are you a general education PK Self-Contained teacher?", ["Yes", "No"])

else:

    # ✅ MULTI-GRADE
    if campus_type == "Elementary":
        grades = st.multiselect("Select grade(s) you teach:", ["K","1","2","3","4","5"])
    elif campus_type == "Intermediate":
        grades = st.multiselect("Select grade(s) you teach:", ["5","6"])
    elif campus_type == "Middle School":
        grades = st.multiselect("Select grade(s) you teach:", ["6","7","8"])
    else:
        grades = st.multiselect("Select grade(s) you teach:", ["9","10","11","12"])

    # ✅ ASSIGNMENT
    assignment = st.radio(
        "Which best describes your teaching assignment?",
        [
            "Math",
            "RLA / Reading",
            "Science",
            "Social Studies",
            "Fine Arts",
            "Foreign Language",
            "CTE",
            "PE",
            "Special Education / Specialized Program"
        ]
    )

    # ✅ ALGEBRA I
    teaches_algebra1 = None
    if assignment == "Math" and campus_type in ["Middle School", "High School"]:
        teaches_algebra1 = st.radio(
            "Do you teach Algebra I (STAAR EOC)?",
            ["Yes","No"]
        )

    # ✅ EOC (HS only)
    teaches_eoc = None
    if campus_type == "High School" and assignment in ["Science","RLA / Reading","Social Studies"]:
        teaches_eoc = st.radio(
            "Do you teach any STAAR EOC courses?",
            ["Biology","English I","English II","U.S. History","None"]
        )

# -----------------------------------
# ✅ RESULT BUTTON (FIXED SYNTAX)
# -----------------------------------
if st.button("Show My Result"):

    if not name or not campus:
        st.error("Please complete required fields.")

    else:

        result_type = "Unknown"

        # ✅ ELC
        if campus_type == "Early Learning Center":
            result_type = "1" if pk_self == "Yes" else "12"

        else:

            # ✅ TYPE 8 PRIORITY
            if teaches_algebra1 == "Yes":
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

            # ✅ TYPE 9 (HS non-EOC)
            elif campus_type == "High School":
                result_type = "9"

            # ✅ OTHER TYPES
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
            "6": "3-8 Math teachers (non-Algebra I).",
            "7": "3-8 RLA teachers.",
            "8": "STAAR and STAAR EOC-tested teachers.",
            "9": "TEKSReady-supported courses.",
            "10": "Physical Education teachers.",
            "11": "SLO-based elective teachers.",
            "12": "Special Programs."
        }

        # -----------------------------------
        # ✅ ASSESSMENTS
        # -----------------------------------
        assessments = {
            "1": "Circle",
            "6": "iReady Math, STAAR VAM",
            "7": "iReady Reading, STAAR VAM",
            "8": "SLOs, STAAR VAM",
            "9": "TEKSReady Pre/Post-Test, SLO",
            "10": "FitnessGram, SLO",
            "11": "SLO",
            "12": "SLO"
        }

        # ✅ STUDENT SURVEY
        if result_type in ["5","6","7","8","9","10","11"]:
            survey = "This teacher type does include a student perception survey for students in grades 3-12."
        else:
            survey = "This teacher type does not include a student perception survey."

        # -----------------------------------
        # ✅ DISPLAY
        # -----------------------------------
        st.success(f"You are TIA Teacher Type {result_type}")

        st.markdown("### Description")
        st.info(descriptions.get(result_type, ""))

        st.markdown("### TIA Assessments")
        st.info(assessments.get(result_type, ""))

        st.markdown("### Student Perception Survey")
        st.info(survey)

        st.markdown(pdf_link)

        # ✅ SAVE
        pd.DataFrame([{
            "Name": name,
            "Campus": campus,
            "Teacher Type": result_type
        }]).to_csv("teacher_results.csv", mode="a", header=False, index=False)
