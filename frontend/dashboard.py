import streamlit as st
from utils import createContainerWithColor
from chart import renderPiechart
from camera import cameraFeed
from control import controlPanel
from metric import fourcolumnsMetric
import os

# Poll the flag file for every 3 seconds
@st.fragment(run_every=3)
def check_for_trigger():
    if os.path.exists("/shared/ping.flag"):
            os.remove("/shared/ping.flag")
            st.rerun()

def show_camera_and_piechart():
    """Helper to display camera feed and pie chart side by side."""
    try:
        good_eggs, dirty_eggs = fourcolumnsMetric()
    except Exception as e:
        st.error(f"Error fetching metrics: {e}")
        good_eggs, dirty_eggs = 0, 0
    mid1, mid2 = st.columns([9, 4])
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

def Dashboard():
    check_for_trigger()
    
    """Main dashboard entry point."""
    st.title("Real-time Monitoring")
    
    show_camera_and_piechart()
    controlPanel()