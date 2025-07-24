import requests
import time
import random

class RealTimePoster:
    def __init__(self, ip: str = "localhost", port: int = 8000):
        self.base_url = f"http://{ip}:{port}"

    def post_real_time(self, good_egg: int, dirty_egg: int, tray_number: int, cam_status: bool, cam_id: int):
        """
        Post real-time data to the backend API.
        """
        url = f"{self.base_url}/real_time/"
        payload = {
            "good_egg": good_egg,
            "dirty_egg": dirty_egg,
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

p = RealTimePoster()


for i in range(1000):
    for j in range(2):
        good_eggs = random.randint(35, 42)
        dirty_eggs = 42 - good_eggs
        cam_status = random.choice([True, False])

        if i % 2 == 0:
            p.post_real_time(good_eggs, dirty_eggs, 1, cam_status, 1)
        else:
            p.post_real_time(good_eggs, dirty_eggs, 1, cam_status, 2)
    time.sleep(1)
