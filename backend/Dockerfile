FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
RUN chmod +x wait-for-it.sh

EXPOSE 8000

CMD ["./wait-for-it.sh", "egg_mysql:3306", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]