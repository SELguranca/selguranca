"""Computer Vision methods."""
from datetime import datetime
from math import ceil
from time import time
import numpy as np
from numpy import uint8
from numpy.typing import NDArray
import cv2


def millis(): return int(round(time() * 1000))


attempts = 0
attempt_treshold = 5
# Type annotation definitions
Frame = NDArray[uint8]


hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def detect_people(frame: Frame) -> tuple[Frame, int]:
    """Run HOG and annotates frame with detected coordinates."""
    width_ratio = 2
    processing_view_width = ceil(640/width_ratio)
    heigth_ratio = 2
    processing_view_height = ceil(480/heigth_ratio)

    processing_frame = cv2.resize(
        frame, (processing_view_width, processing_view_height))
    gray = cv2.cvtColor(processing_frame, cv2.COLOR_RGB2GRAY)
    boxes, _ = hog.detectMultiScale(gray, winStride=(8, 8))
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    current_people = 0 if not boxes.size else len(boxes)

    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(frame, (xA*width_ratio, yA*heigth_ratio), (xB*width_ratio, yB*heigth_ratio),
                      (0, 255, 0), 2)
    if (current_people != detect_people.previous_people):
        detect_people.attempts += 1
        # print("aqui")
        if((millis() - detect_people.last_debounce_time) > 800 or detect_people.attempts > 5):
            print(f"Number of humans in sight: {current_people}")
            detect_people.filtered_people = current_people
            detect_people.previous_people = current_people
            detect_people.attempts = 0

        detect_people.last_debounce_time = millis()

    cv2.rectangle(frame, (10, 10), (245, 45), (60, 60, 60), -1)
    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(frame,
                f"Humans in sight: {detect_people.filtered_people}",
                (20, 35),
                font, 0.7,
                (220, 220, 220),
                2,
                cv2.LINE_4)

    # if (detect_people.previous_people != current_people):
    #     detect_people.previous_people = current_people

    return frame, current_people


# "Static" Variable
detect_people.previous_people = 0
detect_people.filtered_people = 0
detect_people.attempts = 0
detect_people.last_debounce_time = 0


def count_people(frame: Frame) -> int:
    """Run HOG without annotation, just people counting."""
    return 0
