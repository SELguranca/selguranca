"""Flask WebServer."""
from glob import escape
from multiprocessing import Lock
from queue import Queue
import time
from typing import Generator

from flask import Flask
from flask import render_template, Response, request

import Message
from ServoMotor import mH, mV
from ServoController import Controller

app = Flask(__name__)

# Frame Generator Sentinel
please_stop = object()

servo_access = Lock()

controller = Controller(mV, mH)


def start(config: dict) -> None:
    app.run(host=config['host'], port=config['port'],
            debug=True, use_reloader=False)


@app.route('/camera_feed/<string:stream_id>')
def camera_feed_view(stream_id: str) -> Response:
    stream_id = escape(stream_id)

    def frame_generator() -> Generator[bytes, None, None]:
        nonlocal stream_id
        if not Message.Camera.valid_listener(stream_id):
            print(f"Stream '{stream_id}' NOT in listeners, generating...")
            stream_id = Message.Camera.generate()
            yield stream_id.encode('utf-8')
            return

        frames: Queue[bytes] = Queue(maxsize=30)
        Message.Camera.register(stream_id, frames)
        while True:
            frame: bytes = frames.get()
            if frame is please_stop:
                break
            yield (b'--current_frame\r\n'
                   b'Content-Type: image/jpeg\r\n'
                   b'Content-Encoding: gzip\r\n'
                   b'Content-Transfer-Encoding: binary\r\n'
                   b'\r\n' + frame + b'\r\n'
                   b'--current_frame\r\n')

            time.sleep(1/24)

    return app.response_class(frame_generator(), mimetype='multipart/x-mixed-replace; boundary=current_frame')


@app.route("/camera_ctrl/<string:stream_id>/<string:cmd>")
def camera_ctrl(stream_id: str, cmd: str):
    stream_id = escape(stream_id)
    cmd = escape(cmd)
    if cmd == 'stop':
        print(f"Stopping stream: '{stream_id}'")
        Message.Camera.send(stream_id, please_stop)
        Message.Camera.remove(stream_id)
    return Response('0')


@app.route("/controls/request")
def controls_request() -> Response:
    ok = servo_access.acquire(block=False)
    if ok:
        key = Message.Controls.generate()
        print(f"Servo Controls aquired\n\t key: '{key}'")
        return Response(key)
    return Response('-1')


@app.route('/controls/release/')
def controls_release(key: str):
    key = escape(request.headers['Api-Key'])
    if Message.Controls.check(key):
        servo_access.release()
        print(f"Servo Controls released with key: '{key}'")
        Message.Controls.reset()
        return Response('0')
    else:
        return Response('-1')


@app.route('/servo/<string:cmd>')
def servo_view(cmd: str) -> Response:
    cmd = escape(cmd)
    print(f"Recebido comando pro servo: '{cmd}'")
    cmd_e = Message.Command[cmd.upper()]
    _, x, y = controller.consume(cmd_e)
    return Response(f"{x}, {y}")


@app.route("/")
def home() -> Response:
    return render_template('index.html')
