from datetime import datetime
import os
import threading as th
import time
import requests as req
import yaml

import numpy as np
import cv2

import ComputerVision
import Message
import WebServer
from ServoController import Angles


def capture(stop: th.Event, detect: bool, config: dict):
    """Camera frame capture thread."""
    camera = cv2.VideoCapture(config['camera']['device'])
    last_count = -1
    folder = "static/frames"
    isdir = os.path.isdir(folder)
    if not isdir:
        os.mkdir(folder)
    while not stop.wait(0):
        ok, frame = camera.read()
        if not ok or frame is None or np.shape(frame) == ():
            time.sleep(1/config['camera']['fps'])
            continue
        count = -1
        if detect:
            frame, count = ComputerVision.detect_people(frame)
        _, buffer = cv2.imencode('.jpg', frame, params=[
                                 cv2.IMWRITE_JPEG_QUALITY, 75, cv2.IMWRITE_JPEG_OPTIMIZE, 1, cv2.IMWRITE_JPEG_PROGRESSIVE, 1])
        jpeg = buffer.tobytes()

        if(count > 0 and count != last_count):
            now = datetime.now()
            url = f"{folder}/frame_{now.strftime('%Y-%m-%d-%H-%M-%S')}.jpg"
            cv2.imwrite(url, frame)
            horz = WebServer.controller.motors[Angles.PHI].angle
            vert = WebServer.controller.motors[Angles.THETA].angle

            data = {'people_count': count,
                    'time_stamp': now.strftime("%Y-%m-%d-%H:%M:%S"),
                    'horizontal_angle': horz,
                    'vertical_angle': vert,
                    'image': url
                    }
            req.post(
                f"http://{config['server']['host']}:{config['server']['port']}/event", json=data)

        last_count = count
        Message.Camera.broadcast(jpeg)
        time.sleep(1/config['camera']['fps'])
    camera.release()


def main():
    print("----------------\r\n Welcome to SELgurança\r\n----------------\r\n")
    config = {}
    with open("config.yml", 'r') as file:
        config = yaml.load(file, yaml.FullLoader)

    stop = th.Event()
    thread = th.Thread(target=capture, args=(stop, True, config))
    thread.start()
    WebServer.start(config['server'])
    # ...
    stop.set()
    thread.join()


if __name__ == "__main__":
    main()
