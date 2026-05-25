from flask import Flask, render_template, Response, request
import pygame
import cv2
import numpy as np
from game import update_game

app = Flask(__name__)

keys_pressed = set()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/keydown", methods=["POST"])
def keydown():
    key = request.json.get("key")
    keys_pressed.add(key)
    return "", 204


@app.route("/keyup", methods=["POST"])
def keyup():
    key = request.json.get("key")
    keys_pressed.discard(key)
    return "", 204


def generate_frames():

    while True:

        surface = update_game(keys_pressed)

        frame = pygame.surfarray.array3d(surface)

        frame = np.transpose(frame, (1, 0, 2))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        _, buffer = cv2.imencode(".jpg", frame)

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            buffer.tobytes() +
            b"\r\n"
        )


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
