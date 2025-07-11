# eggdashboard

To send images:
    send camera1 image to -> eggdashboard/frontend/images/camera1.jpg
    send camera2 image to -> eggdashboard/frontend/images/camera2.jpg

To send real-time data:
    with this api -> http://0.0.0.0:8000/docs#/default/create_real_time_real_time__post

    Example Value:
        Schema:
        {
            "session_session_id": 0,
            "tray_number": 0,
            "good_egg": 0,
            "dirty_egg": 0,
            "cam1_status": true,
            "cam2_status": true
        }