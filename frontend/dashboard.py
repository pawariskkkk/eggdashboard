import streamlit as st
from utils import createContainerWithColor
from chart import renderPiechart
from camera import cameraFeed
from control import controlPanel
from metric import fourcolumnsMetric

def show_camera_and_piechart():
    """Helper to display camera feed and pie chart side by side."""
    try:
        good_eggs, dirty_eggs = fourcolumnsMetric()
    except Exception as e:
        st.error(f"Error fetching metrics: {e}")
        good_eggs, dirty_eggs = 0, 0
    mid1, mid2 = st.columns([3, 1])
    with mid1:
        camera = createContainerWithColor("camera", "#151717", 1)
        with camera:
            try:
                cameraFeed()
            except Exception as e:
                st.error(f"Camera error: {e}")
    with mid2:
        piechart = createContainerWithColor("piechart", "#151717", 1)
        with piechart:
            st.subheader("Egg Quality Distribution")
            try:
                fig = renderPiechart(good_eggs, dirty_eggs)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Pie chart error: {e}")

#realtime part of dashboard
@st.fragment(run_every="7s")
def realTimePart():
    """Fragment that updates the camera and pie chart every 7 seconds."""
    show_camera_and_piechart()

def Dashboard():
    """Main dashboard entry point."""
    st.title("Real-time Monitoring")
    # Defensive: check if 'started' exists in session_state
    started = st.session_state.get('started', False)
    if started:
        realTimePart()
    else:
        show_camera_and_piechart()
    controlPanel()