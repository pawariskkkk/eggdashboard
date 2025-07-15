# eggdashboard

To send images:
    send camera1 image to -> eggdashboard/frontend/images/camera1.jpg
    send camera2 image to -> eggdashboard/frontend/images/camera2.jpg

To post use postrealtime.py as template

frontend
|-.streamlit: set auto rerun and theme
|-asset: collect image
|-images: get image from camera
|-app.py: main app
|-camera.py: camera components
|-chart.py: chart components
|-control.py: production control at the buttom of dashboard
|-dashboard.py: contain chart, control and camera realtime dashboard page
|-filter.py: contain filter that use for filter datatable
|-datatable.py: contain datatable
|-sidebar.py: sidebar of dashboard and datatable
|-style.css: style sidebar and container
|-utils.py: contain selectbox and function to style each container
|-fetch.py: fetch data from api
|-wait-for-it.sh: to make frontend start after backend

backend
|-database.py: to link with database mysql
|-main.py: fastapi
|-models.py: table models for database
|-wait-for-it.sh: wait for mysql to start first