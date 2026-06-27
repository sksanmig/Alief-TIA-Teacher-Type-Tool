import streamlit as st
import pandas as pd

st.set_page_config(page_title="Teacher Profile Tool", layout="centered")

# -----------------------------------
# ✅ BANNER HEADER (FIXED)
# -----------------------------------
st.markdown(
    """
    <div style="background-color:#008066; padding:15px; border-radius:8px; display:flex; align-items:center;">
        <img src="https://cmsv2-assets.apptegy.net/uploads/20164/logo/22855/AliefSmartChoice.png"
             style="height:60px; margin-right:20px;">
        <div>
            <h2 style="color:white; margin:0;">Alief ISD Teacher Profile Tool</h2>
            <p style="color:white; margin:0;">Determine your TIA Teacher Type</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

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
.stButton>button:hover {
    background-color: #006655;
}
</style>
""", unsafe_allow_html=True)

pdf_link = "[View Full TIA Teacher Type Guide](https://aliefisd-my.sharepoint.com/:b:/g/personal/stefan_sanmiguel_aliefisd_net/IQC3HSJ7-pB_Tp_Go-EsT4k0AX7Blc9bpbaJjk_-ZKZ4V4U?e=voJjZK)"

# -----------------------------------
# INFO
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
            if pk_self == "Yes":
                result_type = "1"
            else:
                result_type = "12"

        else:

            # ✅ TYPE 8
            if teaches_algebra1 == "Yes":
                result_type = "8"

            elif assignment == "Science":
                if "5" in grades or "8" in grades:
                    result_           result_type = "9"

            elif assignment == "Social Studies":
                if "8" in grades:
                    result_type = "8"
                else:
                    result_type = "9"

            elif teaches_eoc is not None and teaches_eoc != "None":
                result_type = "8"

            # ✅ TYPE 6 / 7
            elif assignment == "Math" and any(g in ["3","4","5","6","7","8"] for g in grades):
                result_type = "6"

            elif assignment == "RLA / Reading" and any(g in ["3","4","5","6","7","8"] for g in grades):
                result_type = "7"

            # ✅ TYPE 9 fallback
            elif campus_type == "High School":
                result_type = "9"

            elif assignment == "PE":
                result_type = "10"

            elif assignment == "Special Education / Specialized Program":
                result_type = "12"

            else:
                result_type = "11"

        # DISPLAY
        st.success(f"You are TIA Teacher Type {result_type}")

        st.markdown("### Description")
        st.info("See official document for full description.")

        st.markdown("### TIA Assessments")
        st.info("See official document for assessment details.")

        st.markdown("### Student Perception Survey")
        st.info("Refer to document for survey details.")

        st.markdown(pdf_link)

        pd.DataFrame([{
            "Name": name,
            "Campus": campus,
            "Teacher Type": result_type
        }]).to_csv("teacher_results.csv", mode="a", header=False, index=False)
