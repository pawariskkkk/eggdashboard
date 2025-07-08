import requests
import streamlit as st

BASE_URL = "http://localhost:8000"

def get_session_summary(session_id):
    """
    Fetches the session summary for a given session_id from the backend API.
    Returns a dict with keys: good_egg, dirty_egg, tray_count, cam1_status, cam2_status, cam1_image, cam2_image
    """
    try:
        response = requests.get(f"{BASE_URL}/session/{session_id}/summary")
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "good_egg": 0,
            "dirty_egg": 0,
            "tray_count": 0,
            "cam1_status": None,
            "cam2_status": None,
            "cam1_image": None,
            "cam2_image": None
        }