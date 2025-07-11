import requests
import streamlit as st

BASE_URL = "http://egg_backend:8000"

def get_session_summary(session_id, cam_id):
    """
    Fetches the session summary for a given session_id from the backend API.
    Returns a dict with keys: good_egg, dirty_egg, tray_count, cam_status
    """
    try:
        response = requests.get(f"{BASE_URL}/session/{session_id}/{cam_id}/summary")
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "good_egg": 0,
            "dirty_egg": 0,
            "tray_count": 0,
            "cam_status": None,
        }