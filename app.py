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
            "Interventionist",
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

    # -----------------------------------
    # ICS LOGIC
    # -----------------------------------
    if assignment == "In-Class Support":

        support_content = st.multiselect(
            "What content areas do you support?",
            [
                "Math",
                "RLA",
                "Science",
                "Social Studies",
                "Special Education / Program (Read 180, REACH, LIFE, TLC)",
                "Other"
            ]
        )

        support_grades = st.multiselect(
            "What grade levels do you support?",
            ["K-2","3-4","5","6","7","8","High School"]
        )

    # -----------------------------------
    # INTERVENTIONIST LOGIC
    # -----------------------------------
    if assignment == "Interventionist":

        intervention_type = st.radio(
            "Are you an ELD Interventionist?",
            ["Yes", "No"]
        )

        if intervention_type == "No":
            support_content = st.multiselect(
                "What content areas do you support?",
                ["Math", "RLA", "Science", "Social Studies", "Other"]
            )

            support_grades = st.multiselect(
                "What grade levels do you support?",
                ["3-4","5","6","7","8","High School"]
            )

    # -----------------------------------
    # ✅ ALGEBRA I (Math only)
    # -----------------------------------
    teaches_algebra1 = None
    if assignment == "Math" and campus_type in ["Middle School", "High School"]:
        teaches_algebra1 = st.radio(
            "Do you teach Algebra I (STAAR EOC course)?",
            ["Yes", "No"]
        )

    # -----------------------------------
    # ✅ EOC (HS core non-math)
    # -----------------------------------
    teaches_eoc = None
    if campus_type == "High School" and assignment in ["Science", "RLA / Reading", "Social Studies"]:
        teaches_eoc = st.radio(
            "Do you teach any STAAR EOC courses?",
            ["Biology", "English I", "English II", "U.S. History", "None of these"]
        )

# -----------------------------------
# FINAL RESULT
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

            # ✅ ICS
            if assignment == "In-Class Support":

                sped_option = "Special Education / Program (Read 180, REACH, LIFE, TLC)"

                if len(support_content) == 1 and sped_option in support_content:
                    result_type = "12"

                else:
                    filtered = [c for c in support_content if c != sped_option]

                    if ("Math" in filtered or "RLA" in filtered) and any(g in support_grades for g in ["3-4","5","6","7","8"]):
                        result_type = "8"

                    elif "Science" in filtered and ("5" in support_grades or "8" in support_grades):
                        result_type = "8"

                    elif "Social Studies" in filtered and "8" in support_grades:
                        result_type = "8"

                    elif "High School" in support_grades:
                        result_type = "9"

                    else:
                        result_type = "11"

            # ✅ INTERVENTIONIST
            elif assignment == "Interventionist":

                if intervention_type == "Yes":
                    result_type = "7"

                else:
                    if ("Math" in support_content or "RLA" in support_content) and any(g in support_grades for g in ["3-4","5","6","7","8"]):
                        result_type = "8"

                    elif "High School" in support_grades:
                        result_type = "9"

                    else:
                        result_type = "11"

            # ✅ DYSLEXIA
            elif assignment == "Dyslexia Teacher":
                result_type = "4" if grade in ["K","1","2"] else "7"

            # -----------------------------------
            # ✅ TYPE 8 (STRICT PRIORITY)
            # -----------------------------------
            elif teaches_algebra1 == "Yes":
                result_type = "8"

            elif grade == "5" and assignment == "Science":
                result_type = "8"

            elif grade == "8" and assignment == "Science":
                result_type = "8"

            elif grade == "8" and assignment == "Social Studies":
                result_type = "8"

            elif teaches_eoc is not None and teaches_eoc != "None of these":
                result_type = "8"

            # -----------------------------------
            # ✅ TYPE 6 / 7
            # -----------------------------------
            elif assignment == "Math" and grade in ["3","4","5","6","7","8"]:
                result_type = "6"

            elif assignment == "RLA / Reading" and grade in ["3","4","5","6","7","8"]:
                result_type = "7"

            # -----------------------------------
            # ✅ TYPE 9 (HS NON-EOC)
            # -----------------------------------
            elif campus_type == "High School":
                result_type = "9"

            # -----------------------------------
            # ✅ TYPE 10–12
            # -----------------------------------
            elif assignment == "PE":
                result_type = "10"

            elif assignment == "Special Education / Specialized Program":
                result_type = "12"

            else:
                result_type = "11"

        # -------------------------------
        # DESCRIPTIONS
        # -------------------------------
        descriptions = {
            "1": "PK Self-Contained General Education Teachers.",
            "2": "K-2 Self-Contained (SC) General Education Teachers and In-Class Support Teachers.",
            "3": "K-2 Math, Math/Science General Education Teachers and In-Class Support Teachers.",
            "4": "K-2 RLA, RLA/Social Studies General Education Teachers, In-Class Support Teachers, and Dyslexia Teachers.",
            "5": "3-5 Self-Contained General Education Teachers and In-Class Support Teachers. This type includes a student perception survey.",
            "6": "3-8 Math, Math/Science General Education Teachers and In-Class Support Teachers. This type includes a student perception survey.",
            "7": "3-8 RLA, RLA/Social Studies General Education Teachers, In-Class Support Teachers, Dyslexia Teachers, and ELD Interventionist. This type includes a student perception survey.",
            "8": "5-8 STAAR Science and STAAR Social Studies Teachers, 9-12 STAAR EOC teachers, In-Class Support Teachers, and general Interventionist. This type includes a student perception survey.",
            "9": "3-12 TEKsReady general education and In-Class Support Teachers of non-STAAR core, Elective, or Block Courses. This type includes a student perception survey.",
            "10": "K-12 Physical Education Teachers. Student Growth Measures: This type includes a student perception survey.",
            "11": "3-12 SLO Block and Elective General Education Teachers. This type includes a student perception survey.",
            "12": "Other PK-12 Special Education Teachers (Life, Reach, Read 180), ALC Teachers, ESCE Teachers, or Block ELC Teachers."
        }

        # -------------------------------
        # ASSESSMENTS
        # -------------------------------
        assessments = {
            "1": "Circle",
            "2": "Amplify mClass-RLA, iReady-Math",
            "3": "iReady-Math, STEMScopes",
            "4": "iReady-Reading, Amplify mClass-RLA",
            "5": "iReady-Math, iReady-Reading, STAAR VAM",
            "6": "iReady-Math, Teacher STAAR VAM",
            "7": "iReady-Reading, Teacher STAAR VAM",
            "8": "SLOs, Teacher STAAR VAM",
            "9": "SLO, TEKSReady Pre/Post-Test",
            "10": "SLO, FitnessGram",
            "11": "SLO",
            "12": "SLO"
        }

        # ✅ STUDENT SURVEY
        if result_type in ["5","6","7","8","9","10","11"]:
            survey = "This teacher type does include a student perception survey for students in grades 3-12."
        else:
            survey = "This teacher type does not include a student perception survey."

        # -----------------------------------
        # DISPLAY
        # -----------------------------------
        st.success(f"You are TIA Teacher Type {result_type}")

        st.markdown("### Description")
        st.info(descriptions[result_type])

        st.markdown("### TIA Assessments")
        st.info(assessments[result_type])

        st.markdown("### Student Perception Survey")
        st.info(survey)

        st.markdown(pdf_link)

        # SAVE
        pd.DataFrame([{
            "Name": name,
            "Campus": campus,
            "Teacher Type": result_type
        }]).to_csv("teacher_results.csv", mode="a", header=False, index=False)
