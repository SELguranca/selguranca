from datetime import datetime
import threading
import time
from flask import Flask
import cv2
from queue import Queue
import numpy as np

app = Flask(__name__)
frame_q = Queue(maxsize=60)


@app.route("/")
def hello_world():
    return "<h1>Welcome to SELgurança!</h1><br /><br /><p align='center'><img src='/camera' /> </p >"


live_view_width = 1024
live_view_height = 576

width_ratio = 2
heigth_ratio = 2

processing_view_width = int(live_view_width/width_ratio)
processing_view_height = int(live_view_height/heigth_ratio)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
font = cv2.FONT_HERSHEY_SIMPLEX


# camera = cv2.VideoCapture(0)
def loopao():
    camera = cv2.VideoCapture(1)
    # set new dimensionns to cam object (not cap)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, live_view_width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, live_view_height)
    current_people = 0
    previous_people = 0
    while True:
        # Capture frame-by-frame
        ok, frame = camera.read()
        #  Codigo do HOG
        processing_frame = cv2.resize(
            frame, (processing_view_width, processing_view_height))
        # using a greyscale picture, also for faster detection
        gray = cv2.cvtColor(processing_frame, cv2.COLOR_RGB2GRAY)

        # detect people in the image
        # returns the bounding boxes for the detected objects
        boxes, weights = hog.detectMultiScale(
            processing_frame, winStride=(8, 8))

        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

        if(boxes.size == 0):
            current_people = 0

        for (xA, yA, xB, yB) in boxes:
            current_people = (len(boxes))
            # display the detected boxes in the colour picture
            cv2.rectangle(frame, (xA*width_ratio, yA*heigth_ratio), (xB*width_ratio, yB*heigth_ratio),
                          (0, 255, 0), 2)

            now = datetime.now()

            cv2.putText(frame,
                        f"Humans in sight: {current_people}  Date and time: {now}",
                        (25, 25),
                        font, 0.8,
                        (0, 255, 255),
                        2,
                        cv2.LINE_4)

        if (previous_people != current_people):
            print(f"Number of humans in sight: {current_people}")
            previous_people = current_people
        if ok:
            frame_q.put(frame)


@app.route("/camera")
def camera_view():
    def generate():
        print("Roda uma vez a cada request HTTP")
        while True:
            # Capture frame-by-frame
            # frame = cv2.resize(frame, (640, 320))
            frame = frame_q.get()
            _, buffer = cv2.imencode('.jpg', frame)
            f_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\nContent-Encoding: gzip\r\n\r\n' + f_bytes + b'\r\n')
            # cv2.waitKey(1)
            time.sleep(1/61)

    return app.response_class(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


def main():
    print("----------------\r\n Welcome to SELgurança\r\n----------------\r\n")
    thread = threading.Thread(target=loopao)
    #  ...
    try:
        thread.start()
        app.run(host="0.0.0.0", port="8051", debug=True, use_reloader=False)
        thread.join()
    except:
        camera.release()


if __name__ == "__main__":
    main()
