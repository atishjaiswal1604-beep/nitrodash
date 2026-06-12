FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV SDL_VIDEODRIVER=dummy

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libsdl2-dev \
    libsm6 \
    libxext6 \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
