FROM python:3.11

RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    ffmpeg \
    libsm6 \
    libxext6

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN pip install opencv-python numpy

ENV SDL_VIDEODRIVER=dummy

EXPOSE 5000

CMD ["python", "app.py"]
