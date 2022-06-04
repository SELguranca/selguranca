"""Flask WebServer."""
from queue import Queue
import Message
import time
from typing import Generator
from flask import Flask
from flask import render_template, Response

app = Flask(__name__)


def start() -> None:
    app.run(host="0.0.0.0", port="8051",
                 debug=True, use_reloader=False)


@app.route('/camera_feed')
def camera_feed_view() -> Response:
    def frame_generator() -> Generator[bytes, None, None]:
        my_queue = Queue(maxsize=30)
        Message.Camera.add_listener(my_queue)
        while True:
            frame: bytes = my_queue.get()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\nContent-Encoding: gzip\r\n\r\n' + frame + b'\r\n')

            time.sleep(1/24)

    return app.response_class(frame_generator(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/")
def home() -> Response:
    return render_template('index.html')
