"""Flask WebServer."""
from glob import escape
from queue import Queue
from ComputerVision import Frame
import Message
import time
from typing import Generator
from flask import Flask, request
from flask import render_template, Response
from ServoMotor import mH, mV

app = Flask(__name__)
please_stop = object()


def start() -> None:
    app.run(host="0.0.0.0", port="8051",
                 debug=True, use_reloader=False)


@app.route('/camera_feed')
def camera_feed_view() -> Response:
    def frame_generator() -> Generator[bytes, None, None]:
        my_queue: Queue[bytes] = Queue(maxsize=30)
        index = Message.Camera.add_listener(my_queue)
        while True:
            frame: bytes = my_queue.get()
            if frame == please_stop:
                break
            # stream_id_header: bytes = f"Stream-ID: {index}\r\n".encode("utf-8")
            yield (b'--current_frame\r\n'
                   b'Content-Type: image/jpeg\r\n'
                   b'Content-Encoding: gzip\r\n'
                   b'Content-Transfer-Encoding: binary\r\n'
                #    + stream_id_header +
                   b'\r\n' + frame + b'\r\n'
                   b'--current_frame\r\n')

            time.sleep(1/24)

    return app.response_class(frame_generator(), mimetype='multipart/x-mixed-replace; boundary=current_frame')


@app.route('/servo/<string:cmd>', methods=['GET'])
def servo_view(cmd: str) -> Response:
    if request.method == 'GET':
        cmd = escape(cmd)
        # print(f"Recebido comando pro servo: {cmd}")
        if cmd == "up":
            mV.controle("+")
        elif cmd == "down":
            mV.controle("-")
        elif cmd == "left":
            mH.controle("+")
        elif cmd == "right":
            mH.controle("-")
        elif cmd == "sweep_v":
            mV.Varredura()
        elif cmd == "sweep_h":
            mH.Varredura()
        else:
            pass
        return Response(cmd)
    else:
        return Response("XYZ")

@app.route("/camera_ctrl/<int:id>/<string:cmd>")
def camera_ctrl(id: int, cmd: str):
    if cmd == 'stop':
        Message.Camera.send(id, please_stop)



@app.route("/")
def home() -> Response:
    return render_template('index.html')
