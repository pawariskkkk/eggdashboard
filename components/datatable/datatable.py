import streamlit as st
import pandas as pd
from components.datatable.filter import filter

#to save session between page for input
def secondSessionSave(name):
    st.session_state["%s_save" %name] = st.session_state[name]

#Data table page
def Datatable():
   
    # Layout
    st.set_page_config(layout="wide")
    st.title("📄 Data Table")

    secondSessionSave("tray_amount_dashboard")
    secondSessionSave("farm_dashboard")
    secondSessionSave("house_dashboard")
    secondSessionSave("mfg_dashboard")

    # Sample Data
    df = pd.read_excel("data1.xlsx", sheet_name="mock_egg_data")
    df.columns = ["Date", "Farm", "House", "Manufacturing Date", "Egg Amount", "Dirty Eggs %", "Tray Number"]

    # Convert date columns to datetime
    df["Date"] = pd.to_datetime(df["Date"])
    df["Manufacturing Date"] = pd.to_datetime(df["Manufacturing Date"])

    # Convert House to string for filtering
    df["House"] = df["House"].astype(str)

    #filter function
    date_to, date_from, mfg_from, mfg_to, farm_filter, house_filter, clear_filter, date_filter, mfg_filter = filter()

    # --- Filtering ---
    filtered_df = df.copy()
    filtered_df["Date"] = pd.to_datetime(filtered_df["Date"])
    filtered_df["Manufacturing Date"] = pd.to_datetime(filtered_df["Manufacturing Date"])

    # Date filter
    if date_filter == "Pick a Range" and date_from and date_to:
        filtered_df = filtered_df[
            (filtered_df["Date"] >= pd.to_datetime(date_from)) &
            (filtered_df["Date"] <= pd.to_datetime(date_to))
        ]

    # Manufacturing date filter
    if mfg_filter == "Pick a Range" and mfg_from and mfg_to:
        filtered_df = filtered_df[
            (filtered_df["Manufacturing Date"] >= pd.to_datetime(mfg_from)) &
            (filtered_df["Manufacturing Date"] <= pd.to_datetime(mfg_to))
        ]

    # Optional farm and house filters
    if farm_filter:
        filtered_df = filtered_df[filtered_df["Farm"] == farm_filter]
    if house_filter:
        filtered_df = filtered_df[filtered_df["House"] == house_filter]

    # Clear all filters
    if clear_filter:
        st.session_state["reset_filters_table"] = True
        st.rerun()
        
    # --- Display ---
    st.subheader("📊 Egg Production Data")
    
    # ... then convert to string for display (removes time part visually)
    filtered_df["Date"] = filtered_df["Date"].dt.strftime('%Y-%m-%d')
    filtered_df["Manufacturing Date"] = filtered_df["Manufacturing Date"].dt.strftime('%Y-%m-%d')

    #show table
    st.dataframe(filtered_df, use_container_width=True)

    # --- CSV Export ---
    leftdummy, left_col = st.columns([17, 2])
    with left_col:
        export_df = filtered_df.copy()
        st.download_button(
            "📥 Export as CSV",
            data=export_df.to_csv(index=False),
            file_name="egg_data.csv",
            mime="text/csv"
        )
        
    #let's user recognize the current filter
    st.sidebar.subheader("Current Filters")
    st.sidebar.markdown(f"""
    - **Date:** `{f"{date_from}_{date_to}" if date_from and date_to else "All"}`  
    - **MFG:** `{f"{mfg_from}_{mfg_to}" if mfg_from and mfg_to else "All"}`  
    - **Farm:** `{farm_filter if farm_filter else "All"}`  
    - **House:** `{house_filter if house_filter else "All"}`
    """)