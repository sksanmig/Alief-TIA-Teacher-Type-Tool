import streamlit as st
import pandas as pd

st.set_page_config(page_title="Teacher Profile Tool", layout="centered")

# ✅ SAFE HEADER
st.image(
    "https://cmsv2-assets.apptegy.net/uploads/20164/logo/22855/AliefSmartChoice.png",
    width=180
)

st.title("Alief ISD Teacher Profile Tool")
st.subheader("Determine your TIA Teacher Type")

st.markdown("---")

pdf_link = "[View Full TIA Teacher Type Guide](https://aliefisd-my.sharepoint.com/:b:/g/personal/stefan_sanmiguel_aliefisd_net/IQC3HSJ7-pB_Tp_Go-EsT4k0AX7Blc9bpbaJjk_-ZKZ4V4U?e=voJjZK)"

# -----------------------------------
# INPUTS
# -----------------------------------
name = st.text_input("Enter your name")
campus = st.text_input("Enter your campus")

st.markdown("---")

campus_type = st.radio(
    "What type of campus do you teach at?",
    ["Early Learning Center", "Elementary", "Intermediate", "Middle School", "High School"]
)

# -----------------------------------
# ELC
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
        ["Math","RLA / Reading","Science","Social Studies","PE","Special Education / Specialized Program"]
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
# RESULT
# -----------------------------------
if st.button("Show My Result"):

    if not name or not campus:
        st.error("Please complete required fields.")

    else:

        result_type = "Unknown"

        if campus_type == "Early Learning Center":
            result_type = "1" if pk_self == "Yes" else "12"

        else:

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
        # ✅ FULL DESCRIPTIONS (FROM PDF)
        # -----------------------------------
        descriptions = {
            "1": "PK Self-Contained General Education Teachers.",
            "6": "3-8 Math, Math/Science General Education Teachers. This type includes a student perception survey.",
            "7": "3-8 RLA and Dyslexia Teachers. This type includes a student perception survey.",
            "8": "5-8 STAAR Science, 8th Social Studies, and STAAR EOC teachers. This type includes a student perception survey.",
            "9": "3-12 TEKSReady general education teachers. This type includes a student perception survey.",
            "10": "K-12 Physical Education teachers. This type includes a student perception survey.",
            "11": "3-12 SLO elective teachers. This type includes a student perception survey.",
            "12": "Special Education, ALC, ESCE, or specialized program teachers."
        }

        # -----------------------------------
        # ✅ ASSESSMENTS ONLY
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

        # -----------------------------------
        # ✅ STUDENT SURVEY
        # -----------------------------------
        if result_type in ["5","6","7","8","9","10","11"]:
            survey = "This teacher type does include a student perception survey for students in grades 3-12."
        else:
            survey = "This teacher type does not include a student perception survey."

        # -----------------------------------
        # ✅ DISPLAY
        # -----------------------------------
        st.success(f"You are TIA Teacher Type {result_type}")

        st.markdown("### Description")
        st.info(descriptions.get(result_type, "Description not available"))

        st.markdown("### TIA Assessments")
        st.info(assessments.get(result_type, "Assessment not available"))

        st.markdown("### Student Perception Survey")
        st.info(survey)

        st.markdown(pdf_link)

        # SAVE
        pd.DataFrame([{
            "Name": name,
            "Campus": campus,
            "Teacher Type": result_type
        }]).to_csv("teacher_results.csv", mode="a", header=False, index=False)
