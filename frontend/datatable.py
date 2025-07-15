import streamlit as st
import pandas as pd
from filter import filter
from sqlalchemy import create_engine
from dashboard import check_for_trigger
import os

engine = create_engine(os.getenv("DATABASE_URL"))

#Data table page
def Datatable():
    check_for_trigger()

    # Layout
    st.set_page_config(layout="wide")
    st.title("📄 Data Table")

    
    # Read data from MySQL with error handling
    query = """
        SELECT 
            date AS Date,
            farm AS Farm,
            house AS House,
            mfg AS "Manufacturing Date",
            (COALESCE(good_egg,0) + COALESCE(dirty_egg,0)) AS "Egg Amount",
            CASE 
                WHEN (COALESCE(good_egg,0) + COALESCE(dirty_egg,0)) > 0 THEN 
                    ROUND(COALESCE(dirty_egg,0) * 100.0 / (COALESCE(good_egg,0) + COALESCE(dirty_egg,0)), 2)
                ELSE 0
            END AS "Dirty Eggs %%",
            tray_number AS "Tray Number"
        FROM egg
        WHERE tray_number > 0
    """

    try:
        df = pd.read_sql(query, engine)
        # Convert date columns to datetime
        df["Date"] = pd.to_datetime(df["Date"])
        df["Manufacturing Date"] = pd.to_datetime(df["Manufacturing Date"])
        # Convert House to string for filtering
        df["House"] = df["House"].astype(str)
    except Exception as e:
        # If error, show only the column headers (expected columns)
        columns = [
            "Date", "Farm", "House", "Manufacturing Date",
            "Egg Amount", "Dirty Eggs %", "Tray Number"
        ]
        st.info("Could not load data from database. Displaying column headers only.")
        st.dataframe(pd.DataFrame(columns=columns), use_container_width=True)
        return

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


    # Show table: if no data, show only column headers
    if filtered_df.empty:
        st.info("No data found for the selected filters.")
        st.dataframe(pd.DataFrame(columns=filtered_df.columns), use_container_width=True)
    else:
        filtered_df = filtered_df.sort_index(ascending=False)
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
    st.sidebar.toggle("Real-Time table")