import threading as th
import time
import yaml

import numpy as np
import cv2

import ComputerVision
import Message
import WebServer


def capture(stop: th.Event, detect: bool, config: dict):
    """Camera frame capture thread."""
    camera = cv2.VideoCapture(config['device'])
    while not stop.wait(0):
        ok, frame = camera.read()
        if not ok or frame is None or np.shape(frame) == ():
            time.sleep(1/config['fps'])
            continue

        if detect:
            frame = ComputerVision.detect_people(frame)
        _, buffer = cv2.imencode('.jpg', frame, params=[
                                 cv2.IMWRITE_JPEG_QUALITY, 75, cv2.IMWRITE_JPEG_OPTIMIZE, 1, cv2.IMWRITE_JPEG_PROGRESSIVE, 1])
        jpeg = buffer.tobytes()
        Message.Camera.broadcast(jpeg)
        time.sleep(1/config['fps'])
    camera.release()


def main():
    print("----------------\r\n Welcome to SELgurança\r\n----------------\r\n")
    config = {}
    with open("config.yml", 'r') as file:
        config = yaml.load(file, yaml.FullLoader)

    stop = th.Event()
    thread = th.Thread(target=capture, args=(stop, False, config['camera']))
    thread.start()
    WebServer.start(config['server'])
    # ...
    stop.set()
    thread.join()


if __name__ == "__main__":
    main()
