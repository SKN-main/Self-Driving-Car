
import sys
import time
from imutils.video import JetsonVideoStream, JetsonVideoStreamST
import numpy as np
import cv2
import jetson.utils

from Direction import Direction
import serial
from Car import Car
from flask import Response, Flask


inputWidth = 1280
inputHeight = 720
inputFrameRate = 30

rescaledWidth = 848
rescaledHeight = 480

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.05)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data


def get_frame(input):
    image = input.Capture(format='rgb8')
    imgcvt = jetson.utils.cudaAllocMapped(width=inputWidth, height=inputHeight, format='bgr8')
    jetson.utils.cudaConvertColor(image, imgcvt)

    opencvImage = jetson.utils.cudaToNumpy(imgcvt)
    # return opencvImage[::-1, :, :]
    return opencvImage

# sudo systemctl restart nvargus-daemon


def main():
    car = Car()
    vs = JetsonVideoStream(captureResolution=(inputWidth,inputHeight), outputResolution=(rescaledWidth, rescaledHeight), frameRate=inputFrameRate)
    vs.start()
    time.sleep(2.0)
    action = None

    is_finish = False
    while not is_finish:
        image = vs.read()
        
        mask, frame_with_road_sign, direction, turn_value = car(image)

        # print(turn_value)

        if direction.value == Direction.RIGHT.value:
            action = f'd-{turn_value}'
        elif direction.value == Direction.LEFT.value:
            action = f'a-{turn_value}'
        else:
            action = 'w-0'

        cv2.imshow('Frame', frame_with_road_sign)
        cv2.imshow('Mask', mask)

        key = cv2.waitKey(10) & 0xFF

        if key == ord('q'):
            is_finish = True
            action = 'r-0'
        
        write_read(action)



        # (flag, img) = cv2.imencode(".jpg", mask)
    
        # if not flag:
        #     continue
        
        # yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(img) + b'\r\n')
    vs.stop()
    

app = Flask(__name__)

@app.route("/")
def index():
    return Response(main(), mimetype = "multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    # app.run(host="10.24.224.233", port = 8000, debug = True, threaded = True, use_reloader = False)
    main()

