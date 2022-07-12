"""Flask WebServer."""
import base64
from glob import escape
from multiprocessing import Lock
from queue import Queue
import time
from typing import Generator
import sqlite3 as sql
import json

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


@app.route("/event", methods=['POST', 'GET', 'PUT', 'DELETE'])
def handle_event():
    # return Response(f"Teve um {request.method} no /event")
    # request.args.get

    if(request.method == 'GET'):

        try:
            event_id = request.args.get('id', '')

            with sql.connect("database.db") as con:
                cur = con.cursor()

                cur.execute("SELECT * FROM events WHERE id = ?", event_id)

                msg = cur.fetchone()

                #msg = "Record successfully added :D"

        except:
            msg = "Error in read operation :("

        finally:
            con.close()
            return render_template("results.html", msg=msg)

    elif(request.method == 'POST'):

        data = json.loads(request.data)

        # Just a regular POST:
        if ('action' not in data):

            try:
                event_people_count = data['people_count']
                event_time_stamp = data['time_stamp']
                event_horizontal_angle = data['horizontal_angle']
                event_vertical_angle = data['vertical_angle']
                event_image = data['image']

                con = sql.connect("database.db")
                cur = con.cursor()
                cur.execute("INSERT INTO events (people_count, time_stamp,\
                            horizontal_angle, vertical_angle, image) VALUES (?,?,?,?,?)",
                            (event_people_count, event_time_stamp,
                             event_horizontal_angle, event_vertical_angle, event_image))
                con.commit()


            except Exception as e:
                print(e)
                con.rollback()

            finally:
                con.close()
                return Response("200 OK")

        # If the user sent the 'action' parameter and it was 'UPDATE':
        elif (data['action'] == 'PATCH' or data['action'] == 'UPDATE'):

            try:
                event_id = data['id']
                event_people_count = data['people_count']
                event_time_stamp = data['time_stamp']
                event_horizontal_angle = data['horizontal_angle']
                event_vertical_angle = data['vertical_angle']
                event_image = data['image']

                con = sql.connect("database.db")
                cur = con.cursor()
                cur.execute("UPDATE events SET people_count = ?, \
                            time_stamp = ?, horizontal_angle = ?,\
                            vertical_angle = ?, image = ? WHERE id = ?",
                            (event_people_count, event_time_stamp, event_horizontal_angle,
                             event_vertical_angle, event_image, event_id))
                con.commit()
                print("Record successfully updated :D")
                msg = "Record successfully updated :D"

                # insert or replace into Book (ID, Name, TypeID, Level, Seen) values ((select ID from Book where Name = "SearchName"), "SearchName", ...);

            except Exception as e:
                print(e)
                con.rollback()
                print("Error in updating operation :(")
                msg = "Error in updating operation :("

            finally:
                con.close()
                return render_template("results.html", msg=msg)

        # If the user sent the 'action' parameter and it was 'DELETE':
        elif (data['action'] == 'DELETE'):

            try:
                event_id = data['id']

                #print(f"Event id: {event_id}")

                con = sql.connect("database.db")
                cur = con.cursor()
                # Essa bosta tava dando erro por motivos que eu desconheço. Usei uma gambiarra:
                stringchata = "DELETE FROM events WHERE id = {}".format(
                    event_id)
                cur.execute(stringchata)
                con.commit()

                print("Record successfully deleted :D")
                msg = "Record successfully deleted :D"

            except Exception as e:
                print(e)
                con.rollback()
                print("Error in deleting operation :(")
                msg = "Error in deleting operation :("

            finally:
                con.close()
                return render_template("results.html", msg=msg)


@app.route("/events")
def handle_events():
    # return Response(f"Pediram todo conteudo da tabela")
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row

    cur = conn.cursor()
    cur.execute("select * from events")

    rows = cur.fetchall()
    conn.close()
    return render_template("list.html", rows=rows)
