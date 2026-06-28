import streamlit as st
import pandas as pd
import base64

# -----------------------------------
# Page setup
# -----------------------------------
st.set_page_config(page_title="Teacher Profile Tool", layout="wide")

# -----------------------------------
# Load local Alief logo
# -----------------------------------
with open("Alief Logo.png", "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

# -----------------------------------
# PDF guide link
# -----------------------------------
pdf_link = "https://aliefisd-my.sharepoint.com/:b:/g/personal/stefan_sanmiguel_aliefisd_net/IQC3HSJ7-pB_Tp_Go-EsT4k0AX7Blc9bpbaJjk_-ZKZ4V4U?e=voJjZK"

# -----------------------------------
# Assessment / course lists
# -----------------------------------
staar_courses = ["Algebra I", "Biology", "English I", "English II", "U.S. History"]

base_teks_map = {
    "Math": [
        "Algebra II",
        "Geometry",
        "Math Model Applications (MMA)",
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


def normalize_assignment(assignment_display):
    """Convert campus-specific labels into the internal content area used by the logic."""
    if assignment_display in ["Math", "Math or Math/Science"]:
        return "Math"
    if assignment_display in ["ELA/RLA", "RLA or RLA/Social Studies", "RLA / Reading"]:
        return "RLA / Reading"
    if assignment_display == "Fine and Performing Arts":
        return "Fine Arts"
    if assignment_display == "Language other than English (LOTE)":
        return "Foreign Language"
    if assignment_display == "Physical Education (PE) or Lifetime Pursuits/Activity Teacher":
        return "PE"
    return assignment_display


def get_teksready_courses(content_area, grades):
    """Return only TEKSReady courses that align to selected content area and grade level(s)."""
    if content_area == "Science":
        courses = []
        if "6" in grades:
            courses.append("Science 6")
        if "7" in grades:
            courses.append("Science 7")
        if any(g in ["9", "10", "11", "12"] for g in grades):
            courses.extend([
                "Chemistry I",
                "Physics I / AP Physics I",
                "Aquatic Science",
                "IPC",
                "Environmental Systems",
                "Astronomy"
            ])
        return courses

    if content_area == "Social Studies":
        courses = []
        if "7" in grades:
            courses.append("TX History, Gr 7")
        if any(g in ["9", "10", "11", "12"] for g in grades):
            courses.extend([
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
            ])
        return courses

    return base_teks_map.get(content_area, [])


def any_grade(grades, grade_list):
    return any(g in grade_list for g in grades)


# -----------------------------------
# Layout and styling
# -----------------------------------
left, center, right = st.columns([1, 3, 1])

with center:
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:12px;">
        <img src="data:image/png;base64,{encoded}" style="height:90px;">
    </div>
    <div style="background-color:#008066; padding:18px 20px; margin-bottom:25px; border-radius:10px; text-align:center;">
        <div style="color:white; font-size:30px; font-weight:bold; line-height:1.2;">
            TIA Teacher Type Determination Tool
        </div>
    </div>
    """, unsafe_allow_html=True)

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

    st.markdown(
        "**Directions:** Answer the following guided questions to determine your TIA teacher type and assessment measures for the 2026-2027 school year."
    )

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
    grades = []
    role = None
    assignment = None
    content_area = None
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
            grades = st.multiselect("Select the grade level(s) you instruct:", ["PK", "K", "1", "2", "3", "4", "5"])
        elif campus_type == "Intermediate":
            grades = st.multiselect("Select the grade level(s) you instruct:", ["5", "6"])
        elif campus_type == "Middle School":
            grades = st.multiselect("Select the grade level(s) you instruct:", ["6", "7", "8"])
        else:
            grades = st.multiselect("Select the grade level(s) you instruct:", ["9", "10", "11", "12"])

        role = st.radio(
            "Which best describes your role?",
            [
                "General Education Classroom Teacher",
                "MCT (Model Classroom Teacher)",
                "In-Class Support",
                "Dyslexia Teacher",
                "Interventionist",
                "ALC Teacher",
                "Special Education Teacher (LIFE/REACH/TLC/READ180/Other)"
            ]
        )

        if role == "ALC Teacher":
            auto_result = "Type 12"
        elif role == "Special Education Teacher (LIFE/REACH/TLC/READ180/Other)":
            auto_result = "Type 12"
        elif role == "Interventionist":
            eld_interventionist = st.radio("Are you an ELD Interventionist?", ["Yes", "No"])
            if eld_interventionist == "Yes":
                auto_result = "Type 7"

        if auto_result is None and role != "Dyslexia Teacher":
            if role == "MCT (Model Classroom Teacher)":
                if campus_type == "Elementary":
                    assignment_options = [
                        "Math or Math/Science",
                        "RLA or RLA/Social Studies",
                        "Science",
                        "Social Studies"
                    ]
                else:
                    assignment_options = [
                        "Math",
                        "ELA/RLA",
                        "Science",
                        "Social Studies"
                    ]
            elif campus_type == "Elementary":
                assignment_options = [
                    "Self-Contained General Education",
                    "Math or Math/Science",
                    "RLA or RLA/Social Studies",
                    "Science",
                    "Social Studies",
                    "Fine and Performing Arts",
                    "Language other than English (LOTE)",
                    "Physical Education (PE) or Lifetime Pursuits/Activity Teacher",
                    "Special Education / Specialized Program"
                ]
            else:
                assignment_options = [
                    "Self-Contained General Education",
                    "Math",
                    "ELA/RLA",
                    "Science",
                    "Social Studies",
                    "Fine and Performing Arts",
                    "Language other than English (LOTE)",
                    "CTE",
                    "Physical Education (PE) or Lifetime Pursuits/Activity Teacher",
                    "Special Education / Specialized Program",
                    "Other Elective / Block Course"
                ]

            assignment = st.radio(
                "Which best describes your teaching assignment/content area?",
                assignment_options
            )
            content_area = normalize_assignment(assignment)

            if role == "In-Class Support":
                support_areas = st.multiselect(
                    "What content areas do you support?",
                    ["K-2 Math", "K-2 RLA", "3-8 Math", "3-8 RLA", "STAAR / EOC Courses", "TEKSReady Courses"]
                )

            if content_area == "Math" and campus_type in ["Middle School", "High School"]:
                teaches_algebra1 = st.radio("Do you teach Algebra I?", ["Yes", "No"])

            if campus_type == "High School":
                if content_area == "Science":
                    teaches_eoc = st.radio("Do you teach a STAAR EOC course?", ["Biology", "None"])
                elif content_area == "RLA / Reading":
                    teaches_eoc = st.radio("Do you teach a STAAR EOC course?", ["English I", "English II", "None"])
                elif content_area == "Social Studies":
                    teaches_eoc = st.radio("Do you teach a STAAR EOC course?", ["U.S. History", "None"])

            if teaches_algebra1 == "Yes" or (teaches_eoc in staar_courses):
                eoc_retester_only = st.radio(
                    "Do you teach only retesters or students new to the country taking STAAR for the first time?",
                    ["Yes", "No"]
                )

            if content_area == "Math":
                if teaches_algebra1 == "No" and not any_grade(grades, ["K", "1", "2", "3", "4", "5", "6", "7", "8"]):
                    show_teksready = True

            elif content_area in ["RLA / Reading", "Science", "Social Studies", "Fine Arts", "Foreign Language", "CTE"]:
                is_eoc = teaches_eoc in staar_courses
                is_staar_science = content_area == "Science" and any_grade(grades, ["5", "8"])
                is_staar_social_studies = content_area == "Social Studies" and "8" in grades
                is_3_8_rla = content_area == "RLA / Reading" and any_grade(grades, ["3", "4", "5", "6", "7", "8"])
                is_k_2_rla = content_area == "RLA / Reading" and any_grade(grades, ["K", "1", "2"])

                if not is_eoc and not is_staar_science and not is_staar_social_studies and not is_3_8_rla and not is_k_2_rla:
                    show_teksready = True

            # Elementary MCTs cannot be TEKSReady teachers.
            if show_teksready and not (role == "MCT (Model Classroom Teacher)" and campus_type == "Elementary"):
                teksready_options = get_teksready_courses(content_area, grades)
                if len(teksready_options) > 0:
                    selected_teks = st.multiselect(
                        "Do you teach any of these courses? Select all that apply.",
                        teksready_options
                    )

    # -----------------------------------
    # Final classification
    # -----------------------------------
    if st.button("Show My Result"):

        if not name or not campus:
            st.error("Please fill in required fields.")
        elif campus_type != "Early Learning Center" and len(grades) == 0:
            st.error("Please select at least one grade level.")
        else:
            result = "Unknown"

            if campus_type == "Early Learning Center":
                result = "Type 1" if pk_self == "Yes" else "Type 12"

            else:
                if auto_result is not None:
                    result = auto_result

                elif role == "Dyslexia Teacher":
                    if any_grade(grades, ["3", "4", "5", "6", "7", "8"]):
                        result = "Type 7"
                    elif any_grade(grades, ["K", "1", "2"]):
                        result = "Type 4"
                    else:
                        result = "Type 11"

                elif content_area == "Special Education / Specialized Program":
                    result = "Type 12"

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

                elif role == "Interventionist" and eld_interventionist == "Yes":
                    result = "Type 7"

                elif content_area == "Self-Contained General Education":
                    if any_grade(grades, ["3", "4", "5"]):
                        result = "Type 5"
                    elif any_grade(grades, ["K", "1", "2"]):
                        result = "Type 2"
                    elif "PK" in grades:
                        result = "Type 1"
                    else:
                        result = "Unknown"

                if result == "Unknown":
                    if teaches_algebra1 == "Yes":
                        result = "Type 11" if eoc_retester_only == "Yes" else "Type 8"

                    elif teaches_eoc in staar_courses:
                        result = "Type 11" if eoc_retester_only == "Yes" else "Type 8"

                    elif "5" in grades and content_area == "Science":
                        result = "Type 8"

                    elif "8" in grades and content_area == "Science":
                        result = "Type 8"

                    elif "8" in grades and content_area == "Social Studies":
                        result = "Type 8"

                    elif content_area == "Math" and any_grade(grades, ["K", "1", "2"]):
                        result = "Type 3"

                    elif content_area == "RLA / Reading" and any_grade(grades, ["K", "1", "2"]):
                        result = "Type 4"

                    elif content_area == "Math" and any_grade(grades, ["3", "4", "5", "6", "7", "8"]):
                        result = "Type 6"

                    elif content_area == "RLA / Reading" and any_grade(grades, ["3", "4", "5", "6", "7", "8"]):
                        result = "Type 7"

                    elif len(selected_teks) > 0:
                        result = "Type 9"

                    elif content_area == "PE":
                        result = "Type 10"

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
