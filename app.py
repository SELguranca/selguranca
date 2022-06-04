import threading as th
import time
import cv2

import ComputerVision
import Message
import WebServer


def capture(stop: th.Event):
    camera = cv2.VideoCapture(1)
    while not stop.wait(0):
        ok, frame = camera.read()
        if not ok:
            time.sleep(1/10)
            continue
        # frame = ComputerVision.detect_people(frame)
        _, buffer = cv2.imencode('.jpg', frame)
        jpeg = buffer.tobytes()
        Message.Camera.send(jpeg)
        time.sleep(1/24)
    camera.release()


def main():
    print("----------------\r\n Welcome to SELgurança\r\n----------------\r\n")
    stop = th.Event()
    thread = th.Thread(target=capture, args=(stop,))
    thread.start()
    WebServer.start()
    # ...
    stop.set()
    thread.join()


if __name__ == "__main__":
    main()
