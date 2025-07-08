import streamlit as st
from datetime import date
from datetime import date, timedelta
import pandas as pd
from utils import farmSelectbox

#last week and last month function
def shortcutDate(label="lastweek"):
    if st.session_state.get(f"{label}_filters_table"):
        st.session_state["date_selectbox_table"] = "Pick a Range"
        st.session_state["date_from_table"] = date.today() - timedelta(days=7 if label=="lastweek" else 30)
        st.session_state["date_to_table"] = date.today()
        st.session_state[f"{label}_filters_table"] = False

#all table filter
def filter():
    # Before rendering widgets
    if st.session_state.get("reset_filters_table"):
        st.session_state["date_selectbox_table"] = "All Dates"
        st.session_state["mfg_selectbox_table"] = "All Dates"
        st.session_state["farm_filter_table"] = ""
        st.session_state["house_table"] = ""
        st.session_state["reset_filters_table"] = False  # Clear the flag

    shortcutDate()
    shortcutDate("lastmonth")

    # --- Filter UI ---
    c1, c2, c3 = st.columns(3)
    date_filter = c1.selectbox("Date", ["All Dates", "Pick a Range"], key="date_selectbox_table")
    
    with c1:
        filter1, filter2 = st.columns(2)
        if date_filter == "Pick a Range":
            date_from = filter1.date_input("Date From", key="date_from_table")
            date_to = filter2.date_input("Date To", key="date_to_table")
        else:
            date_from = None
            date_to = None

    mfg_filter = c2.selectbox("MFG", ["All Dates", "Pick a Range"], key="mfg_selectbox_table")
    with c2:
        filter1, filter2 = st.columns(2)
        if mfg_filter == "Pick a Range":
            mfg_from = filter1.date_input("MFG From", key="mfg_from_table")
            mfg_to = filter2.date_input("MFG To", key="mfg_to_table")
        else:
            mfg_from = None
            mfg_to = None
    with c3:
        filter1, filter2 = st.columns(2)
        farm_filter = farmSelectbox(filter1, False, "farm_filter_table")
        house_filter = filter2.selectbox("House", [""] + [str(i) for i in range(1, 17)], key="house_table")

    # --- Filter Buttons ---
    b1, b2, *_, b11 = st.columns(11)
    with b1:
        lweek = st.button("Last Week")
    with b2:
        lmonth = st.button("Last Month")
    with b11:
        clear_filter = st.button("Clear Filters")

    # --- Date shortcuts ---
    if lweek:
        st.session_state["lastweek_filters_table"] = True
        st.rerun()
    
    if lmonth:
        st.session_state["lastmonth_filters_table"] = True
        st.rerun()
        
    return date_to, date_from, mfg_from, mfg_to, farm_filter, house_filter, clear_filter, date_filter, mfg_filter