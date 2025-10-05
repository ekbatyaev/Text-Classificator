FROM python:3.9

WORKDIR /AI_SERVER

# Установка системных зависимостей
RUN apt-get update && apt-get install -y git

# Установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir protobuf==3.20.0

COPY . .

EXPOSE 8140

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8140"]