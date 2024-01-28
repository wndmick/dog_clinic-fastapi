FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 5555

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5555"]

# docker build -t dog-clinic-fastapi .
# docker run -d -p 5555:5555 dog-clinic-fastapi