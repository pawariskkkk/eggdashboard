import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"  # or use public IP/domain when deployed

# Example: Fetch data from backend
def get_data():
    response = requests.get(f"{API_BASE_URL}/data")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data")
        return {}

# Example: Submit form/input data to backend
def submit_data(payload):
    response = requests.post(f"{API_BASE_URL}/submit", json=payload)
    if response.status_code == 200:
        st.success("Data submitted successfully")
    else:
        st.error("Failed to submit data")