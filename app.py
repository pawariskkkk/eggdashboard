import streamlit as st
from components.sidebar import sidebar

# Page setup
st.set_page_config(layout="wide")
# CSS Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
        
sidebar()