import streamlit as st
from utils import createContainerWithColor
from fetch import get_session_summary

#each metric component
def metric(name, top, down, label, pic, head):
    name = createContainerWithColor(name)
    with name:
        icon1, icon2 = st.columns([3, 1])
        with icon1:
            st.metric(head, label)
        with icon2:
            st.image(f"assets/{pic}", width=70)
        
        st.progress(top / down if top <= down else 1/1)

#to save session between page for input
def firstSessionSave(name):
    if name not in st.session_state and ("%s_save" %name in st.session_state):
        st.session_state[name] = st.session_state["%s_save" %name]
    
def fourcolumnsMetric():
    
    firstSessionSave("tray_amount_dashboard")
    firstSessionSave("farm_dashboard")
    firstSessionSave("house_dashboard")
    firstSessionSave("mfg_dashboard")
    
    if "tray_amount_dashboard" not in st.session_state:
        st.session_state.tray_amount_dashboard = 150
    if "trays_goal" not in st.session_state:
        st.session_state.trays_goal = 150
    if "egg_goal" not in st.session_state:
        st.session_state.egg_goal = 150 * 42
    
    # Fetch session summary if session_id exists
    trays_processed = 0
    good_eggs = 0
    dirty_eggs = 0
    if "session_id" in st.session_state:
        summary = get_session_summary(st.session_state["session_id"])
        trays_processed = summary["tray_count"]
        good_eggs = summary["good_egg"]
        dirty_eggs = summary["dirty_egg"]
    dirty_expected = 500
    reject_target = 5.0

    # --- Metrics with progress ---
    col1, col2, col3, col4 = st.columns(4)

    trays_goal = st.session_state.trays_goal
    egg_goal = st.session_state.egg_goal
    reject_rate = round((dirty_eggs*100)/egg_goal, 1) if egg_goal else 0
    with col1:
        metric("mt1", trays_processed, trays_goal, f"{trays_processed}/{trays_goal}", "layers.png", "Trays Processed")

    with col2:
        metric("mt2", good_eggs, egg_goal, f"{good_eggs}/{egg_goal}", "eggs.png", "Good Eggs")

    with col3:
        metric("mt3", dirty_eggs, dirty_expected, f"{dirty_eggs}", "no.png", "Dirty Eggs")

    with col4:
        metric("mt4", reject_rate, reject_target, f"{reject_rate}%", "pie-chart.png", "Rejection Rate")
            
    return good_eggs, dirty_eggs