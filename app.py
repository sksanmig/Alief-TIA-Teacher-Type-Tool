import streamlit as st
import pandas as pd

# ✅ Page setup
st.set_page_config(page_title="Teacher Profile Tool", layout="wide")

# -----------------------------------
# ✅ GREEN BANNER (NO HTML RISK)
# -----------------------------------
banner_left, banner_right = st.columns([2, 5])

with banner_left:
    st.image("Alief Logo.png", width=260)

with banner_right:
    st.markdown(
        """
        <h2 style='color:#008066; margin-bottom:0;'>Alief ISD Teacher Profile Tool</h2>
        <p style='margin-top:0;'>Determine your TIA Teacher Type</p>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ✅ PDF LINK
pdf_link = "[View Full TIA Teacher Type Guide](https://aliefisd-my.sharepoint.com/:b:/g/personal/stefan_sanmiguel_aliefisd_net/IQC3HSJ7-pB_Tp_Go-EsT4k0AX7Blc9bpbaJjk_-ZKZ4V4U?e=voJjZK)"

# -----------------------------------
# ✅ CENTER CONTENT
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
        pk_self = st.radio("Are you a PK Self-Contained teacher?", ["Yes", "No"])

    else:
        if campus_type == "Elementary":
            grades = st.multiselect("Grades:", ["K","1","2","3","4","5"])
        elif campus_type == "Intermediate":
            grades = st.multiselect("Grades:", ["5","6"])
        elif campus_type == "Middle School":
            grades = st.multiselect("Grades:", ["6","7","8"])
        else:
