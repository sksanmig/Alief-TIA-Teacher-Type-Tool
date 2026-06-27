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
# ELC
# -----------------------------------
if campus_type == "Early Learning Center":
    pk_self = st.radio("Are you a general education PK Self-Contained teacher?", ["Yes","No"])

else:

    # ✅ MULTI-GRADE SELECTION
    if campus_type == "Elementary":
        grades = st.multiselect("Select grade(s) you teach:", ["K","1","2","3","4","5"])
    elif campus_type == "Intermediate":
        grades = st.multiselect("Select grade(s) you teach:", ["5","6"])
    elif campus_type == "Middle School":
        grades = st.multiselect("Select grade(s) you teach:", ["6","7","8"])
    else:
        grades = st.multiselect("Select grade(s) you teach:", ["9","10","11","12"])

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

    # ICS
    if assignment == "In-Class Support":
        support_content = st.multiselect(
            "What content areas do you support?",
            ["Math","RLA","Science","Social Studies",
             "Special Education / Program (Read 180, REACH, LIFE, TLC)","Other"]
        )
        support_grades = st.multiselect(
            "What grade levels do you support?",
            ["K-2","3-4","5","6","7","8","High School"]
        )

    # Interventionist
    if assignment == "Interventionist":
        intervention_type = st.radio("Are you an ELD Interventionist?", ["Yes","No"])
        if intervention_type == "No":
            support_content = st.multiselect(
                "What content areas do you support?",
                ["Math","RLA","Science","Social Studies","Other"]
            )
            support_grades = st.multiselect(
                "What grade levels do you support?",
                ["3-4","5","6","7","8","High School"]
            )

    # Algebra I
    teaches_algebra1 = None
    if assignment == "Math" and campus_type in ["Middle School","High School"]:
        teaches_algebra1 = st.radio("Do you teach Algebra I (STAAR EOC course)?", ["Yes","No"])

    # HS EOC
    teaches_eoc = None
    if campus_type == "High School" and assignment in ["Science","RLA / Reading","Social Studies"]:
        teaches_eoc = st.radio(
            "Do you teach any STAAR EOC courses?",
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

            # ✅ ICS
            if assignment == "In-Class Support":
                sped = "Special Education / Program (Read 180, REACH, LIFE, TLC)"

                if len(support_content) == 1 and sped in support_content:
                    result_type = "12"
                else:
                    filtered = [c for c in support_content if c != sped]

                    if ("Math" in filtered or "RLA" in filtered):
                        result_type = "8"
                    elif "High School" in support_grades:
                        result_type = "9"
                    else:
                        result_type = "11"

            # ✅ Interventionist
            elif assignment == "Interventionist":

                if intervention_type == "Yes":
                    result_type = "7"

                else:
                    if ("Math" in support_content or "RLA" in support_content):
                        result_type = "8"
                    elif "High School" in support_grades:
                        result_type = "9"
                    else:
                        result_type = "11"

            # ✅ Dyslexia
            elif assignment == "Dyslexia Teacher":
                if any(g in ["K","1","2"] for g in grades):
                    result_type = "4"
                else:
                    result_type = "7"

            # ✅ Algebra I
            elif teaches_algebra1 == "Yes":
                result_type = "8"

            # ✅ Science (NEW MULTI-GRADE LOGIC)
            elif assignment == "Science":
                if "5" in grades or "8" in grades:
                    result_type = "8"
                else:
                    result_type = "9"

            # ✅ Social Studies (NEW MULTI-GRADE LOGIC)
            elif assignment == "Social Studies":
                if "8" in grades:
                    result_type = "8"
                elif "7" in grades:
                    result_type = "9"

            # ✅ HS EOC
            elif teaches_eoc is not None and teaches_eoc != "None":
                result_type = "8"

            # ✅ Math
            elif assignment == "Math" and any(g in ["3","4","5","6","7","8"] for g in grades):
                result_type = "6"

            # ✅ RLA
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

        # Basic display
        st.success(f"You are TIA Teacher Type {result_type}")
        st.markdown(pdf_link)

        pd.DataFrame([{
            "Name": name,
            "Campus": campus,
            "Teacher Type": result_type
        }]).to_csv("teacher_results.csv", mode="a", header=False, index=False)
