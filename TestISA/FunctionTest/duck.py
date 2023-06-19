import cv2
import numpy as np
from Direction import Direction

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)


def track_car(frame):
    biggest_iou = 0
    position_x = frame.shape[1]//2
    direction = Direction.STRAIGHT
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([78,158,124])
    upper = np.array([138,255,255])

    mask = cv2.inRange(image, lower, upper)

    blur = cv2.GaussianBlur(mask,(25,25),0)
    thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)[1]

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        iou = w*h/(frame.shape[0]*frame.shape[1])
        if iou > biggest_iou:
            biggest_iou = iou
            position_x = x+w//2
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,255), 2)

    deviation = abs(position_x - frame.shape[1]//2)/(frame.shape[1]//2)

    if position_x < frame.shape[1]//2:
        direction = Direction.LEFT
    elif position_x > frame.shape[1]//2:
        direction = Direction.RIGHT

    cv2.putText(frame, f"{direction.name}", (100, 100), 2, 3, (0, 0, 255), 2)
    cv2.putText(frame, f"{round(deviation, 2)}", (100, 150), 2, 3, (0, 0, 255), 2)

    return direction, deviation

while cap.isOpened():
    _, original = cap.read()
    _, mask = track_car(original)
    
    cv2.imshow('original', original)
    cv2.imshow('mask', mask)


    cv2.waitKey(10)