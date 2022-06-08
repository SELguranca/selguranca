import threading as th
import numpy as np
import time
import cv2

import ComputerVision
import Message
import WebServer


def capture(stop: th.Event, fps: int, detect: bool):
    """Camera frame capture thread."""
    camera = cv2.VideoCapture(1)
    while not stop.wait(0):
        ok, frame = camera.read()
        if not ok or frame is None or np.shape(frame) == ():
            time.sleep(1/fps)
            continue

        if detect:
            frame = ComputerVision.detect_people(frame)

        _, buffer = cv2.imencode('.jpg', frame, params=[
                                 cv2.IMWRITE_JPEG_QUALITY, 75, cv2.IMWRITE_JPEG_OPTIMIZE, 1, cv2.IMWRITE_JPEG_PROGRESSIVE, 1])
        jpeg = buffer.tobytes()
        Message.Camera.send(jpeg)
        cv2.waitKey(1000//fps)
    camera.release()


def main():
    print("----------------\r\n Welcome to SELgurança\r\n----------------\r\n")
    stop = th.Event()
    thread = th.Thread(target=capture, args=(stop, 12, False))
    thread.start()
    WebServer.start()
    # ...
    stop.set()
    thread.join()


if __name__ == "__main__":
    main()
