import streamlit as st
import pandas as pd

st.set_page_config(page_title="Teacher Profile Tool", layout="centered")

# -----------------------------------
# ✅ HEADER (SAFE)
# -----------------------------------
col1, col2 = st.columns([1, 3])

with col1:
    st.image(
        "https://cmsv2-assets.apptegy.net/uploads/20164/logo/22855/AliefSmartChoice.png",
        width=120
    )

with col2:
    st.markdown(
        "<h2 style='color:#008066; margin-bottom:0;'>Alief ISD Teacher Profile Tool</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='margin-top:0;'>Determine your TIA Teacher Type</p>",
        unsafe_allow_html=True
    )

st.markdown("---")

# -----------------------------------
# ✅ GREEN STYLING
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
        border: 2px solid #008066 !important;
        border-radius: 6px;
    }

    .stRadio > div {
        border: 2px solid #008066;
        padding: 10px;
        border-radius: 8px;
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
# LINK
# -----------------------------------
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

            # ✅ SELF-CONTAINED
            if assignment == "Self-Contained General Education":
                if any(g in ["3","4","5"] for g in grades):
                    result_type = "5"
                elif any(g in ["K","1","2"] for g in grades):
                    result_type = "2"

            # ✅ TYPE 8 PRIORITY
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

            # ✅ TYPE 6 / 7
