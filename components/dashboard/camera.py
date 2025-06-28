import streamlit as st

#get camera status
def cameraStatus(number="camera1_status"):
    if True or st.session_state[number]:
        return "🟢"
    else:
        return "🔴"

#main camera component
def cameraFeed():
    subh1, subh2 = st.columns([3, 1])
    with subh1:
        st.subheader("Live Camera Feed")
    with subh2:
        sepcam1, sepcam2 = st.columns([1,3])
        sepcam2.write(f"{cameraStatus()} camera1 {cameraStatus("camera2_status")} camera2")
    fcam1, fcam2 = st.columns(2)
    with fcam1:
        st.image("assets/eggxample.jpg", width=520)
    with fcam2:
        st.image("assets/eggxample.jpg", width=520)