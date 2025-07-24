import time
import random
from postrealtime import RealTimePoster

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
