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
# TEKSReady course lists
# -----------------------------------
staar_courses = ["Algebra I", "Biology", "English I", "English II", "U.S. History"]

teks_map = {
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
    "Foreign Language": [
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
# Layout and styling
# -----------------------------------
left, center, right = st.columns([1, 3, 1])

with center:
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
    # Teacher info
    # -----------------------------------
    name = st.text_input("Enter your name")
    campus = st.text_input("Enter your campus")

    st.markdown("---")

    campus_type = st.radio(
        "What type of campus do you teach at?",
        ["Early Learning Center", "Elementary", "Intermediate", "Middle School", "High School"]
    )

    # Defaults
    pk_self = None
    grade = None
    role = None
    assignment = None
    support_areas = []
    eld_interventionist = None
    auto_result = None
    teaches_algebra1 = None
    teaches_eoc = None
    eoc_retester_only = None
    selected_teks = []
    show_teksready = False

    if campus_type == "Early Learning Center":
        pk_self = st.radio("Are you a general education PK Self-Contained teacher?", ["Yes", "No"])

    else:
        if campus_type == "Elementary":
            grade = st.selectbox("Grade:", ["K", "1", "2", "3", "4"])
        elif campus_type == "Intermediate":
            grade = st.selectbox("Grade:", ["5", "6"])
        elif campus_type == "Middle School":
            grade = st.selectbox("Grade:", ["7", "8"])
        else:
            grade = st.selectbox("Grade:", ["9", "10", "11", "12"])

        role = st.radio(
            "Which best describes your role?",
            [
                "General Education Classroom Teacher",
                "In-Class Support",
                "Dyslexia Teacher",
                "Interventionist",
                "ALC Teacher",
                "ESCE Teacher",
                "Life / Reach / Read 180 Teacher",
                "Block ELC Teacher",
                "Other Special Education Teacher",
                "Other"
            ]
        )

        # Auto-route ALC teachers without displaying the result early
        if role == "ALC Teacher":
            auto_result = "Type 12"

        # Interventionist ELD follow-up without displaying the result early
        elif role == "Interventionist":
            eld_interventionist = st.radio("Are you an ELD Interventionist?", ["Yes", "No"])
            if eld_interventionist == "Yes":
                auto_result = "Type 7"

        # Do not ask additional questions if already auto-classified
        if auto_result is None:
            assignment = st.radio(
                "Which best describes your teaching assignment/content area?",
                [
                    "Self-Contained General Education",
                    "Math",
                    "RLA / Reading",
                    "Science",
                    "Social Studies",
                    "Fine Arts",
                    "Foreign Language",
                    "CTE",
                    "PE",
                    "Special Education / Specialized Program",
                    "Other Elective / Block Course"
                ]
            )

            # In-Class Support logic
            if role == "In-Class Support":
                support_areas = st.multiselect(
                    "What content areas do you support?",
                    ["K-2 Math", "K-2 RLA", "3-8 Math", "3-8 RLA", "STAAR / EOC Courses", "TEKSReady Courses"]
                )

            # Algebra I
            if assignment == "Math" and campus_type in ["Middle School", "High School"]:
                teaches_algebra1 = st.radio("Do you teach Algebra I?", ["Yes", "No"])

            # EOC
            if assignment in ["Science", "Social Studies", "RLA / Reading"] and campus_type == "High School":
                teaches_eoc = st.radio("Do you teach STAAR EOC courses?", staar_courses + ["None"])

            # EOC/Algebra I retester/newcomer follow-up
            if teaches_algebra1 == "Yes" or (teaches_eoc in staar_courses):
                eoc_retester_only = st.radio(
                    "Do you teach only retesters or students new to the country taking STAAR for the first time?",
                    ["Yes", "No"]
                )

            # TEKSReady course logic
            # Math: if not Algebra I, show TEKSReady Math courses when not already K-8 Math.
            if assignment == "Math":
                if teaches_algebra1 == "No" and grade not in ["K", "1", "2", "3", "4", "5", "6", "7", "8"]:
                    show_teksready = True

            elif assignment in ["RLA / Reading", "Science", "Social Studies", "Fine Arts", "Foreign Language", "CTE"]:
                is_eoc = teaches_eoc in staar_courses
                is_staar_science = assignment == "Science" and grade in ["5", "8"]
                is_staar_social_studies = assignment == "Social Studies" and grade == "8"
                is_3_8_rla = assignment == "RLA / Reading" and grade in ["3", "4", "5", "6", "7", "8"]
                is_k_2_rla = assignment == "RLA / Reading" and grade in ["K", "1", "2"]

                if not is_eoc and not is_staar_science and not is_staar_social_studies and not is_3_8_rla and not is_k_2_rla:
                    show_teksready = True

            if show_teksready and assignment in teks_map:
                selected_teks = st.multiselect(
                    "Select TEKSReady courses you teach:",
                    teks_map[assignment]
                )

    # -----------------------------------
    # Final classification
    # -----------------------------------
    if st.button("Show My Result"):

        if not name or not campus:
            st.error("Please fill in required fields.")
        else:
            result = "Unknown"

            if campus_type == "Early Learning Center":
                result = "Type 1" if pk_self == "Yes" else "Type 12"

            else:
                if auto_result is not None:
                    result = auto_result

                elif role in ["ESCE Teacher", "Life / Reach / Read 180 Teacher", "Block ELC Teacher", "Other Special Education Teacher"]:
                    result = "Type 12"

                elif assignment == "Special Education / Specialized Program":
                    result = "Type 12"

                # In-Class Support rules
                elif role == "In-Class Support":
                    if "STAAR / EOC Courses" in support_areas:
                        result = "Type 8"
                    elif "3-8 Math" in support_areas:
                        result = "Type 6"
                    elif "3-8 RLA" in support_areas:
                        result = "Type 7"
                    elif "K-2 Math" in support_areas:
                        result = "Type 3"
                    elif "K-2 RLA" in support_areas:
                        result = "Type 4"
                    elif "TEKSReady Courses" in support_areas:
                        result = "Type 9"
                    else:
                        result = "Type 11"

                # Interventionist rules
                elif role == "Interventionist" and eld_interventionist == "Yes":
                    result = "Type 7"

                # Dyslexia
                elif role == "Dyslexia Teacher":
                    result = "Type 4" if grade in ["K", "1", "2"] else "Type 7"

                # Self-contained / General Education Classroom Teacher
                elif assignment == "Self-Contained General Education" or role == "General Education Classroom Teacher":
                    if grade in ["K", "1", "2"]:
                        result = "Type 2"
                    elif grade in ["3", "4", "5"]:
                        result = "Type 5"
                    else:
                        # If a high school/secondary general education classroom teacher is not self-contained,
                        # continue through the content rules below by temporarily leaving result unknown.
                        result = "Unknown"

                # Continue if general education classroom teacher was not classified by self-contained grades
                if result == "Unknown":
                    # Algebra I / EOC with retester-newcomer rule
                    if teaches_algebra1 == "Yes":
                        result = "Type 11" if eoc_retester_only == "Yes" else "Type 8"

                    elif teaches_eoc in staar_courses:
                        result = "Type 11" if eoc_retester_only == "Yes" else "Type 8"

                    # STAAR Type 8
                    elif grade == "5" and assignment == "Science":
                        result = "Type 8"

                    elif grade == "8" and assignment == "Science":
                        result = "Type 8"

                    elif grade == "8" and assignment == "Social Studies":
                        result = "Type 8"

                    # Type 3 / 4 / 6 / 7
                    elif assignment == "Math" and grade in ["K", "1", "2"]:
                        result = "Type 3"

                    elif assignment == "RLA / Reading" and grade in ["K", "1", "2"]:
                        result = "Type 4"

                    elif assignment == "Math" and grade in ["3", "4", "5", "6", "7", "8"]:
                        result = "Type 6"

                    elif assignment == "RLA / Reading" and grade in ["3", "4", "5", "6", "7", "8"]:
                        result = "Type 7"

                    # Type 9 TEKSReady
                    elif len(selected_teks) > 0:
                        result = "Type 9"

                    # Type 10 PE
                    elif assignment == "PE":
                        result = "Type 10"

                    # Default elective/block
                    else:
                        result = "Type 11"

            type_number = result.replace("Type ", "")

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
                if type_number in ["5", "6", "7", "8", "9", "10", "11"]
                else "This teacher type does NOT include a student perception survey."
            )

            pd.DataFrame([{"Name": name, "Campus": campus, "Type": result}]).to_csv(
                "teacher_results.csv", mode="a", header=False, index=False
            )

            st.success(f"Your TIA Teacher Type: {result}")

            st.markdown("### Description")
            st.info(descriptions.get(type_number, ""))

            st.markdown("### TIA Assessments")
            st.info(assessments.get(type_number, ""))

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
