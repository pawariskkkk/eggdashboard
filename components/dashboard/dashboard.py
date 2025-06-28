import streamlit as st
from utils import createContainerWithColor
from components.dashboard.chart import renderPiechart
from components.dashboard.camera import cameraFeed
from components.dashboard.control import controlPanel
from components.dashboard.metric import fourcolumnsMetric

def Dashboard():
    st.title("Real-time Monitoring")

    good_eggs, dirty_eggs = fourcolumnsMetric()
    
    mid1, mid2 = st.columns([3, 1])
    with mid1:
        camera = createContainerWithColor("camera", "#151717", 1)
        with camera:
            cameraFeed()

    with mid2:
        piechart = createContainerWithColor("piechart", "#151717", 1)
        with piechart:
            st.subheader("Egg Quality Distribution")
            fig = renderPiechart(good_eggs, dirty_eggs)
            st.plotly_chart(fig, use_container_width=True)
    
    controlPanel()