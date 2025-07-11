import streamlit as st
from datetime import datetime
from utils import createContainerWithColor, farmSelectbox
import requests

#to make real time update for metric component
def updateGoals():
    st.session_state.trays_goal = st.session_state.tray_amount_dashboard
    st.session_state.egg_goal = st.session_state.tray_amount_dashboard * 42

#disable the input button when start or stop is clicked
def inputDisable(state=True):
    st.session_state.disabled_farm = state
    st.session_state.disabled_house = state
    st.session_state.disabled_mfg = state
    st.session_state.disabled_eggs = state

#input button
def inputButton(disabled_farm, disabled_house, disabled_mfg, disabled_eggs):
    input1, input2, input3, input4 = st.columns(4)
    with input1:
        farm = farmSelectbox(input1, disabled_farm, "farm_dashboard")
        st.session_state["farm_dashboard_save"] = farm
    with input2:
        house = st.selectbox("House", [""] + list(map(str, range(1, 17))), disabled=disabled_house, key="house_dashboard")
        st.session_state["house_dashboard_save"] = house
    with input3:
        mfg_date = st.date_input("Manufacturing Date", disabled=disabled_mfg, key="mfg_dashboard")
        st.session_state["mfg_dashboard_save"] = mfg_date
    with input4:
        tray_amount = st.number_input(
            "Trays Amount",
            min_value=1,
            step=1,
            key="tray_amount_dashboard",
            on_change=updateGoals,
            disabled=disabled_eggs
        )
        st.session_state["tray_amount_dashboard_save"] = tray_amount
            
    return farm, house, mfg_date, tray_amount

#all control and input panel
def controlPanel():
    
    #initial disabled button session_state if it not
    if "disabled_farm" not in st.session_state:
        st.session_state.disabled_farm = False
    if "disabled_house" not in st.session_state:
        st.session_state.disabled_house = False
    if "disabled_mfg" not in st.session_state:
        st.session_state.disabled_mfg = False
    if "disabled_eggs" not in st.session_state:
        st.session_state.disabled_eggs = False
        
    #assign value from session_state
    disabled_farm = st.session_state.disabled_farm
    disabled_house = st.session_state.disabled_house
    disabled_mfg = st.session_state.disabled_mfg
    disabled_eggs = st.session_state.disabled_eggs
    
    # --- Input Section (above buttons) ---

    if "starttime" not in st.session_state:
        st.session_state.starttime = None
    if "session_id" not in st.session_state:
        st.session_state.session_id = None

    inputty = createContainerWithColor("inputty", "#151717" , 1)
    with inputty:
        st.subheader("Production Controls")
        
        farm, house, mfg_date, tray_amount = inputButton(disabled_farm, disabled_house, disabled_mfg, disabled_eggs)

        # --- Start / Stop / Reset Controls ---
        if "started" not in st.session_state:
            st.session_state.started = False

        if "stopped" not in st.session_state:
            st.session_state.stopped = False

        ctrl1, ctrl2, ctrl3 = st.columns([1, 1, 1])

        # Disable Start if required fields are missing
        start_disabled = not (farm and house and mfg_date and tray_amount > 0)

        with ctrl1:
            if st.button("▶️ Start", disabled=start_disabled, use_container_width=True):
                st.session_state.stopped = True
                if ("have_stopped" not in st.session_state) or st.session_state["have_stopped"] == False:
                    # Prepare data for API
                    data = {
                        "date": datetime.now().isoformat(),
                        "farm": farm,
                        "house": house,
                        "mfg": mfg_date.isoformat(),
                        "tray_amount": tray_amount
                    }
                    try:
                        response = requests.post("http://egg_backend:8000/session/", json=data)
                        response.raise_for_status()
                        session_id = response.json()["session_id"]
                        st.session_state["session_id"] = session_id
                    except Exception as e:
                        st.error(f"Failed to create session: {e}")
                        st.stop()
                    st.session_state.starttime = datetime.now()
                    
                inputDisable()
                st.session_state.started = True
                st.session_state["show_success"] = True
                st.session_state["show_stopped"] = False
                st.rerun()

            if st.session_state.get("show_success"):
                st.success("Production Started")
        with ctrl2:
            if st.session_state.stopped:
                if st.button("⏹ Stop", use_container_width=True):
                    st.session_state.started = False
                    st.session_state["show_stopped"] = True
                    st.session_state["show_success"] = False
                    st.session_state["have_stopped"] = True
                    st.rerun()

            if st.session_state.get("show_stopped"):
                    st.warning("Production Stopped")
        with ctrl3:
            if not st.session_state.started and st.session_state.stopped:
                if st.button("🔄 Reset", use_container_width=True):
                    inputDisable(False)
                    st.session_state.stopped = False
                    st.session_state["show_success"] = False
                    st.session_state["show_stopped"] = False
                    st.session_state["have_stopped"] = False
                    st.rerun()
                    
    starttime = st.session_state.starttime
    session_id = st.session_state.session_id
    st.sidebar.subheader("Current Session")
    st.sidebar.markdown(f"""
        - **Session_id:** `{session_id if session_id else "not defined"}`
        - **StartAt:** `{starttime.date() if starttime else "not defined"}`
        - **Farm:** `{farm if farm else "not defined"}`  
        - **House:** `{house if house else "not defined"}`  
        - **MFG:** `{mfg_date}` 
        - **TrayAmount:** `{tray_amount}`
        """)