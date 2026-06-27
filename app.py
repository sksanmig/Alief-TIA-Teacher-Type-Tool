import streamlit as st
import pandas as pd

st.set_page_config(page_title="Teacher Profile Tool", layout="centered")

# -----------------------------------
# ✅ ALIEF BANNER HEADER
# -----------------------------------
st.markdown(
    """
    <div style="
        background-color: #008066;
        padding: 15px;
        border-radius: 8px;
        display: flex;
        align-items: center;">
        
        <img src="https://cmsv2-assets.apptegy.net/uploads/20164/logo/22855/AliefSmartChoice.png"
             style="height:60px; margin-right:20px;">
        
        <div>
            <h2 style="color:white; margin:0;">
                Alief ISD Teacher Profile Tool
            </h2>
            <p style="color:white; margin:0;">
                Determine your TIA Teacher Type
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# -----------------------------------
# ✅ CUSTOM STYLING (STEP 3)
# -----------------------------------
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #008066;
        color: white;
