import streamlit as st
from components.dashboard.dashboard import Dashboard
from components.datatable.datatable import Datatable
from streamlit_option_menu import option_menu

#sidebar
def sidebar():
    st.sidebar.image("assets/logo.png", width=280)
    
    with st.sidebar:
        selected=option_menu(
            menu_title="Menu",
            icons=["layout-sidebar", "table"],
            options=["Dashboard","Data Table"],
        )
        
    if selected == "Dashboard":
        Dashboard()
    elif selected == "Data Table":
        Datatable()
    