import streamlit as st
import base64

# ✅ PAGE CONFIG
st.set_page_config(page_title="Teacher Profile Tool", layout="wide")

# -----------------------------------
# ✅ HEADER
# -----------------------------------
with open("Alief Logo.png", "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

st.markdown(f"""
<div style="background-color:#008066; padding:20px; margin-bottom:25px;">
    <div style="max-width:1100px; margin:auto; display:flex; align-items:center;">
        <img src="data:image/png;base64,{encoded}" style="height:70px; margin-right:25px;">
        <div>
            <div style="color:white; font-size:28px; font-weight:bold;">
                Alief ISD Teacher Profile Tool
            </div>
            <div style="color:white; font-size:16px;">
                Determine your TIA Teacher Type
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ✅ PDF LINK
pdf_link = "https://aliefisd-my.sharepoint.com/:b:/g/personal/stefan_sanmiguel_aliefisd_net/IQC3HSJ7-pB_Tp_Go-EsT4k0AX7Blc9bpbaJjk_-ZKZ4V4U?e=voJjZK"

# -----------------------------------
# ✅ CENTER LAYOUT
# -----------------------------------
left, center, right = st.columns([1, 3, 1])

with center:

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
        padding: 10px;
        border-radius: 8px;
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

        # ✅ FOLLOW-UP LOGIC
        retester_only = None
        if (
            (teaches_eoc is not None and teaches_eoc != "None")
            or teaches_algebra1 == "Yes"
        ):
            retester_only = st.radio(
                "Do you teach only retesters or students new to the country taking STAAR for the first time?",
                ["Yes","No"]
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

                if assignment == "Self-Contained General Education":
                    if any(g in ["3","4","5"] for g in grades):
                        result_type = "5"
                    elif any(g in ["K","1","2"] for g in grades):
                        result_type = "2"

                elif teaches_algebra1 == "Yes":
                    result_type = "11" if retester_only == "Yes" else "8"

                elif teaches_eoc is not None and teaches_eoc != "None":
                    result_type = "11" if retester_only == "Yes" else "8"

                elif assignment == "Science":
                    result_type = "8" if ("5" in grades or "8" in grades) else "9"

                elif assignment == "Social Studies":
                    result_type = "8" if "8" in grades else "9"

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
            # ✅ OUTPUT BOXES
            # -----------------------------------
            descriptions = {
                "1": "PK Self-Contained General Education Teachers.",
                "2": "K-2 Self-Contained General Education Teachers.",
                "5": "3-5 Self-Contained Teachers.",
                "6": "3-8 Math Teachers.",
                "7": "3-8 RLA Teachers.",
                "8": "STAAR-tested teachers including EOC courses.",
                "9": "TEKSReady-supported teachers.",
                "10": "PE Teachers.",
                "11": "Retesters / SLO teachers.",
                "12": "Special Programs teachers."
            }

            assessments = {
                "1": "Circle",
                "2": "Amplify, iReady",
                "5": "iReady + STAAR VAM",
                "6": "iReady Math + STAAR VAM",
                "7": "iReady Reading + STAAR VAM",
                "8": "SLOs + STAAR VAM",
                "9": "TEKSReady + SLO",
                "10": "FitnessGram + SLO",
                "11": "SLO",
                "12": "SLO"
            }

            survey = (
                "Includes a student perception survey."
                if result_type in ["5","6","7","8","9","10","11"]
                else "Does NOT include a student perception survey."
            )

            st.success(f"You are TIA Teacher Type {result_type}")

            st.markdown("### Description")
            st.info(descriptions.get(result_type,""))

.markdown("### Assessments")
            st.info(assessments.get(result_type,""))

            st.markdown("### Student Survey")
            st.info(survey)

            st.link_button("Open Full TIA Teacher Type Guide", pdf_link)
