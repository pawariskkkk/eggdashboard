import requests
import streamlit as st

BASE_URL = "http://egg_backend:8000"

def get_session_summary(cam_id):
    """
    Fetches the session summary for a given session_id from the backend API.
    Returns a dict with keys: good_egg, dirty_egg, tray_count, cam_status
    """
    try:
        response = requests.get(f"{BASE_URL}/session/{cam_id}/summary")
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "good_egg": 0,
            "dirty_egg": 0,
            "tray_count": 0,
            "cam_status": None,
        }
        
def get_table_summary(table_name):
    try:
        response = requests.get(f"{BASE_URL}/table_summary/{table_name}")
        response.raise_for_status()
        return response.json()
    except Exception:
        st.warning(f"Failed to load data")
        return []
        