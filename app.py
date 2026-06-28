import streamlit as st
import pandas as pd
import base64

# -----------------------------------
# Page setup
# -----------------------------------
st.set_page_config(page_title="Teacher Profile Tool", layout="wide")

# -----------------------------------
# Green banner with local Alief logo
# -----------------------------------
with open("Alief Logo.png", "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

st.markdown(f"""
<div style="background-color:#008066; padding:20px; margin-bottom:25px;">
    <div style="max-width:1100px; margin:auto; display:flex; align-items:center;">
        <img src="data:image/png;base64,{encoded}" style="height:70px; margin-right:25px;">
        <div>
            <div style="color:white; font-size:30px; font-weight:bold;">
                Alief ISD Teacher Profile Tool
            </div>
            <div style="color:white; font-size:18px;">
                Determine your TIA Teacher Type
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# PDF guide link
# -----------------------------------
pdf_link = "https://aliefisd-my.sharepoint.com/:b:/g/personal/stefan_sanmiguel_aliefisd_net/IQC3HSJ7-pB_Tp_Go-EsT4k0AX7Blc9bpbaJjk_-ZKZ4V4U?e=voJjZK"

# -----------------------------------
# TEKSReady course lists by content area
# Source: Alief 26-27 TIA Teacher Type and Assessment List.pdf
# -----------------------------------
TEKSREADY_COURSES = {
    "Math": [
        "Algebra II",
        "Geometry",
        "MMA",
        "Precalculus / AP Precalculus",
        "Statistics / AP Statistics",
        "Algebraic Reasoning"
    ],
    "RLA / Reading": [
        "English III",
        "AP English III (AP Lang)",
        "English IV",
        "AP English IV (AP Lit)"
    ],
    "Science": [
        "Science 6",
        "Science 7",
        "Chemistry I",
        "Physics I / AP Physics I",
        "Aquatic Science",
        "IPC",
        "Environmental Systems",
        "Astronomy"
    ],
    "Social Studies": [
        "TX History, Gr 7",
        "World History / AP World History",
        "World Geography",
        "US Government / AP Government",
        "Economics / Economics OnRamps",
        "Psychology / AP Psychology",
        "Personal Financial Literacy",
        "Sociology",
        "Personal Finan. Lit. & Econ.",
        "African American Studies",
        "Mexican American Studies"
    ],
    "Fine Arts": [
        "General Music, Gr 3",
        "General Music, Gr 5",
        "Art, Gr 5",
        "Art I (HS)",
        "Music I (HS)",
        "Band",
        "Orchestra",
        "Choir/Choral",
        "Tech Theatre I"
    ],
    "World Languages": [
        "Spanish I",
        "Spanish II",
        "French I",
        "French II"
    ],
    "CTE": [
        "Anatomy & Physiology",
        "Audio Video Production I",
        "Culinary Arts",
        "Floral Design",
        "Business Info Management",
        "Fundamentals in Computer Science",
        "Graphic Design & Illustr I",
        "Introduction to Welding",
        "Medical Terminology",
        "Principles of Ag, Food, Natural Res.",
        "Principles of Applied Engineer",
        "Principles of Bus Market Finance",
        "Principles of Health Science",
        "Principles of Hospitality Tour"
    ]
}

# -----------------------------------
# Layout
# -----------------------------------
left, center, right = st.columns([1, 3, 1])

with center:

    # -----------------------------------
    # Styling
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
    # Inputs
    # -----------------------------------
    name = st.text_input("Enter your name")
    campus = st.text_input("Enter your campus")

    st.markdown("---")

    campus_type = st.radio(
        "What type of campus do you teach at?",
        ["Early Learning Center", "Elementary", "Intermediate", "Middle School", "High School"]
    )

    # Defaults so variables always exist
    pk_self = None
    grades = []
    teacher_role = None
    assignment = None
    teaches_algebra1 = None
    teaches_eoc = None
    retester_only = None
    is_eld_interventionist = False
    teksready_courses_selected = []
    should_ask_teksready = False

    # Defaults for logic flags
    is_self_contained_role = False
    is_in_class_support = False
    is_interventionist = False
    is_dyslexia = False
    is_alc_or_special_program = False
    is_algebra_eoc = False
    is_eoc_course = False
    is_staar_science = False
    is_staar_social_studies = False
    is_3_8_math = False
    is_3_8_rla = False
    is_k_2_math = False
    is_k_2_rla = False
    is_self_contained_assignment = False
    is_pe = False
    is_special_program_assignment = False
    is_k_2_dyslexia = False
    is_3_8_dyslexia = False

    if campus_type == "Early Learning Center":
        pk_self = st.radio("Are you a PK Self-Contained teacher?", ["Yes", "No"])

    else:
        if campus_type == "Elementary":
            grades = st.multiselect("Grades:", ["K", "1", "2", "3", "4", "5"])
        elif campus_type == "Intermediate":
            grades = st.multiselect("Grades:", ["5", "6"])
        elif campus_type == "Middle School":
            grades = st.multiselect("Grades:", ["6", "7", "8"])
        else:
            grades = st.multiselect("Grades:", ["9", "10", "11", "12"])

        teacher_role = st.radio(
            "What best describes your role?",
            [
                "Self-Contained General Education Teacher",
                "In-Class Support Teacher",
                "Interventionist",
                "Dyslexia Teacher",
                "ALC Teacher",
                "ESCE Teacher",
                "Life / Reach / Read 180 Teacher",
                "Block ELC Teacher",
                "Other Special Education Teacher"
            ]
        )

        if teacher_role == "Interventionist":
            eld_response = st.radio("Are you an ELD Interventionist?", ["Yes", "No"])
            is_eld_interventionist = eld_response == "Yes"

        assignment = st.radio(
            "Assignment / Content Area",
            [
                "Self-Contained General Education",
                "Math",
                "RLA / Reading",
                "Science",
                "Social Studies",
                "Fine Arts",
                "World Languages",
                "CTE",
                "PE",
                "Special Education / Specialized Program",
                "Other Elective / Block Course"
            ]
        )

        if assignment == "Math" and campus_type in ["Middle School", "High School"]:
            teaches_algebra1 = st.radio("Teach Algebra I?", ["Yes", "No"])

        if campus_type == "High School" and assignment in ["Science", "RLA / Reading", "Social Studies"]:
            teaches_eoc = st.radio(
                "Teach EOC course?",
                ["Biology", "English I", "English II", "U.S. History", "None"]
            )

        # Identify role groups
        is_self_contained_role = teacher_role == "Self-Contained General Education Teacher"
        is_in_class_support = teacher_role == "In-Class Support Teacher"
        is_interventionist = teacher_role == "Interventionist"
        is_dyslexia = teacher_role == "Dyslexia Teacher"
        is_alc_or_special_program = teacher_role in [
            "ALC Teacher",
            "ESCE Teacher",
            "Life / Reach / Read 180 Teacher",
            "Block ELC Teacher",
            "Other Special Education Teacher"
        ]

        # Identify STAAR / EOC / core conditions
        is_algebra_eoc = teaches_algebra1 == "Yes"
        is_eoc_course = teaches_eoc is not None and teaches_eoc != "None"
        is_staar_science = assignment == "Science" and ("5" in grades or "8" in grades)
        is_staar_social_studies = assignment == "Social Studies" and "8" in grades
        is_3_8_math = assignment == "Math" and any(g in ["3", "4", "5", "6", "7", "8"] for g in grades)
        is_3_8_rla = assignment == "RLA / Reading" and any(g in ["3", "4", "5", "6", "7", "8"] for g in grades)
        is_k_2_math = assignment == "Math" and any(g in ["K", "1", "2"] for g in grades)
        is_k_2_rla = assignment == "RLA / Reading" and any(g in ["K", "1", "2"] for g in grades)
        is_self_contained_assignment = assignment == "Self-Contained General Education"
        is_pe = assignment == "PE"
        is_special_program_assignment = assignment == "Special Education / Specialized Program"
        is_k_2_dyslexia = is_dyslexia and any(g in ["K", "1", "2"] for g in grades)
        is_3_8_dyslexia = is_dyslexia and any(g in ["3", "4", "5", "6", "7", "8"] for g in grades)

        # Follow-up for STAAR EOC / Algebra I
        if is_eoc_course or is_algebra_eoc:
            retester_only = st.radio(
                "Do you teach only retesters or students new to the country taking STAAR for the first time?",
                ["Yes", "No"]
            )

        # Explicit TEKSReady candidate logic
        # Math: if they do NOT teach Algebra I and are not K-8 math, show Math TEKSReady list.
        is_math_teksready_candidate = (
            assignment == "Math"
            and teaches_algebra1 == "No"
            and not is_3_8_math
            and not is_k_2_math
        )

        # Other TEKSReady content areas: only if not already classified by STAAR/EOC/K-8 core logic.
        is_non_math_teksready_candidate = (
            assignment in ["RLA / Reading", "Science", "Social Studies", "Fine Arts", "World Languages", "CTE"]
            and not is_eoc_course
            and not is_staar_science
            and not is_staar_social_studies
            and not is_3_8_rla
            and not is_k_2_rla
        )

        should_ask_teksready = (
            not is_alc_or_special_program
            and not is_self_contained_role
            and not is_self_contained_assignment
            and not is_pe
            and not is_special_program_assignment
            and not is_algebra_eoc
            and not is_k_2_dyslexia
            and not is_3_8_dyslexia
            and not is_eld_interventionist
            and (is_math_teksready_candidate or is_non_math_teksready_candidate)
            and assignment in TEKSREADY_COURSES
        )

        if should_ask_teksready:
            teksready_courses_selected = st.multiselect(
                "Select any TEKSReady-supported courses you teach. If none apply, leave this blank.",
                TEKSREADY_COURSES[assignment]
            )

    # -----------------------------------
    # Result logic
    # -----------------------------------
    if st.button("Show My Result"):

        if not name or not campus:
            st.error("Please complete required fields.")

        else:
            result_type = "Unknown"

            if campus_type == "Early Learning Center":
                result_type = "1" if pk_self == "Yes" else "12"

            else:
                if is_alc_or_special_program or is_special_program_assignment:
                    result_type = "12"

                elif is_self_contained_role or is_self_contained_assignment:
                    if any(g in ["3", "4", "5"] for g in grades):
                        result_type = "5"
                    elif any(g in ["K", "1", "2"] for g in grades):
                        result_type = "2"
                    else:
                        result_type = "12"

                elif is_algebra_eoc:
                    result_type = "11" if retester_only == "Yes" else "8"

                elif is_eoc_course:
                    result_type = "11" if retester_only == "Yes" else "8"

                elif is_staar_science:
                    result_type = "8"

                elif is_staar_social_studies:
                    result_type = "8"

                elif is_3_8_math:
                    result_type = "6"

                elif is_3_8_rla or is_3_8_dyslexia or is_eld_interventionist:
                    result_type = "7"

                elif is_k_2_math:
                    result_type = "3"

                elif is_k_2_rla or is_k_2_dyslexia:
                    result_type = "4"

                elif is_pe:
                    result_type = "10"

                elif should_ask_teksready:
                    result_type = "9" if len(teksready_courses_selected) > 0 else "12"

                else:
                    result_type = "11"

            descriptions = {
                "1": "PK Self-Contained General Education Teachers.",
                "2": "K-2 Self-Contained (SC) General Education Teachers and In-Class Support Teachers.",
                "3": "K-2 Math, Math/Science General Education Teachers and In-Class Support Teachers.",
                "4": "K-2 RLA, RLA/Social Studies General Education Teachers, In-Class Support Teachers, and Dyslexia Teachers.",
                "5": "3-5 Self-Contained General Education Teachers and In-Class Support Teachers. This type includes a student perception survey.",
                "6": "3-8 Math, Math/Science General Education Teachers and In-Class Support Teachers. This type includes a student perception survey.",
                "7": "3-8 RLA, RLA/Social Studies General Education Teachers, In-Class Support Teachers, Dyslexia Teachers, and ELD Interventionists. This type includes a student perception survey.",
                "8": "5-8 STAAR Science and STAAR Social Studies Teachers, 9-12 STAAR EOC Teachers, In-Class Support Teachers, and general Interventionists. This type includes a student perception survey.",
                "9": "3-12 TEKSReady general education and In-Class Support Teachers of non-STAAR core, elective, or block courses. This type includes a student perception survey.",
                "10": "K-12 Physical Education Teachers. This type includes a student perception survey.",
                "11": "3-12 SLO block and elective general education teachers, or teachers of only STAAR retesters/newcomers taking STAAR for the first time. This type includes a student perception survey.",
                "12": "Other PK-12 Special Education Teachers, ALC Teachers, ESCE Teachers, Life/Reach/Read 180 Teachers, or Block ELC Teachers."
            }

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

            survey = (
                "This teacher type DOES include a student perception survey for students in grades 3-12."
                if result_type in ["5", "6", "7", "8", "9", "10", "11"]
                else "This teacher type does NOT include a student perception survey."
            )

            st.success(f"You are TIA Teacher Type {result_type}")

            st.markdown("### Description")
            st.info(descriptions.get(result_type, ""))

            st.markdown("### TIA Assessments")
            st.info(assessments.get(result_type, ""))

            st.markdown("### Student Perception Survey")
            st.info(survey)

            st.link_button("Open Full TIA Teacher Type Guide", pdf_link)

            st.markdown("""
            <button onclick="window.print()" style="
                background-color:#008066;
                color:white;
                padding:10px 20px;
                border:none;
                border-radius:8px;
                font-weight:bold;
                cursor:pointer;
                margin-top:15px;
            ">
                Print My Results
            </button>
            """, unsafe_allow_html=True)
