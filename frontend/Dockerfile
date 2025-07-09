FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY frontend/ .
RUN chmod +x wait-for-it.sh

EXPOSE 8501

CMD ["./wait-for-it.sh", "egg_backend:8000", "--", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
