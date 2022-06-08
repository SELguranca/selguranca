"""Flask WebServer."""
from queue import Queue
from ComputerVision import Frame
import Message
import time
from typing import Generator
from flask import Flask, request
from flask import render_template, Response

app = Flask(__name__)


def start() -> None:
    app.run(host="0.0.0.0", port="8051",
                 debug=True, use_reloader=False)


@app.route('/camera_feed')
def camera_feed_view() -> Response:
    def frame_generator() -> Generator[bytes, None, None]:
        my_queue: Queue[bytes] = Queue(maxsize=30)
        Message.Camera.add_listener(my_queue)
        while True:
            frame: bytes = my_queue.get()
            yield (b'--current_frame\r\n'
                   b'Content-Type: image/jpeg\r\n'
                   b'Content-Encoding: gzip\r\n'
                   b'Content-Transfer-Encoding: binary\r\n'
                   b'\r\n' + frame + b'\r\n'
                   b'--current_frame\r\n')

            time.sleep(1/24)

    return app.response_class(frame_generator(), mimetype='multipart/x-mixed-replace; boundary=current_frame')


@app.route('/servo', methods=['GET', 'POST'])
def servo_view() -> Response:
    if request.method == 'POST':
        user_input_command: str = request.form.get('cmd')
        if user_input_command:
            cmd = user_input_command.split('=')[-1]
            print(f"[SERVO] - User commanded: {cmd}")
        print(request.form)
        return Response(f"Command received: {user_input_command}")
    elif request.method == 'GET':
        return Response("ABC")
    else:
        return Response("XYZ")


@app.route("/")
def home() -> Response:
    return render_template('index.html')
