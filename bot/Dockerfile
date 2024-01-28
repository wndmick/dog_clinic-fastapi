FROM python:3.9-slim

WORKDIR /bot

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .

EXPOSE 8000

CMD ["python", "bot.py"]

# docker build -t dog-clinic-bot .
# docker run -d -p 8000:8000 dog-clinic-bot