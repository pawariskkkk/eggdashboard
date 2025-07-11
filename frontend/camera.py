import streamlit as st
from fetch import get_session_summary
import requests

# get camera status from API summary
def cameraStatus(status):
    if status is True:
        return "🟢"
    elif status is False:
        return "🔴"
    else:
        return "⚪"

# main camera component
def cameraFeed():
    cam1_status = None
    cam2_status = None
    cam1_image = "images/camera1.jpg"
    cam2_image = "images/camera2.jpg"
    if "session_id" in st.session_state:
        summary = get_session_summary(st.session_state["session_id"])
        cam1_status = summary["cam1_status"]
        cam2_status = summary["cam2_status"]

    subh1, subh2 = st.columns([27, 10])
    with subh1:
        st.subheader("Live Camera Feed")
    with subh2:
        sepcam1, sepcam2 = st.columns([1,3])
        sepcam2.write(f"{cameraStatus(cam1_status)} camera1 {cameraStatus(cam2_status)} camera2")
    
    fcam1, fcam2 = st.columns(2)
    with fcam1:
        if cam1_image:
            st.image(cam1_image, width=450)
        else:
            st.image("assets/camnotavailable.jpg", width=450)
    with fcam2:
        if cam2_image:
            st.image(cam2_image, width=450)
        else:
            st.image("assets/camnotavailable.jpg", width=450)