import requests

class RealTimePoster:
    def __init__(self, ip: str = "localhost", port: int = 8000):
        self.base_url = f"http://{ip}:{port}"

    def post_real_time(self, good_egg: int, dirty_egg: int, session_id: int, tray_number: int, cam_status: bool, cam_id: int):
        """
        Post real-time data to the backend API.
        """
        url = f"{self.base_url}/real_time/"
        payload = {
            "good_egg": good_egg,
            "dirty_egg": dirty_egg,
            "session_session_id": session_id,
            "tray_number": tray_number,
            "cam_status": cam_status,
            "cam_id": cam_id
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print("Failed to post data:", e)
            return None
