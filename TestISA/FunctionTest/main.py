
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


# arduino = serial.Serial(port='/dev/ttyACM0', baudrate=12412470, timeout=.01)
# arduino = serial.Serial(port='/dev/ttyACM0')

inputWidth = 1280
inputHeight = 720
inputFrameRate = 60

rescaledWidth = 848
rescaledHeight = 480

# arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.05)

# def write_read(x):
#     arduino.write(bytes(x, 'utf-8'))
#     time.sleep(0.05)
#     data = arduino.readline()
#     return data


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
    # camera_input = jetson.utils.videoSource("csi://0", argv=[  "--input-flip=rotate-180", # currently error in library makes it impossible to use this option 
    #                                               "--input-rate={}".format(inputFrameRate), # "--input-rtsp-latency=100", 
    #                                               "--input-width={}".format(inputWidth), "--input-height={}".format(inputHeight)])
    vs = JetsonVideoStream(captureResolution=(inputWidth,inputHeight), outputResolution=(rescaledWidth, rescaledHeight), frameRate=inputFrameRate)
    vs.start()
    time.sleep(2.0)
    action = None

    is_finish = False

    is_finish = False
    while not is_finish:
        # image = get_frame(vs)
        image = vs.read()
        
        mask, frame_with_road_sign, direction, turn_value = car(image)
        print(turn_value)
        
        if direction.value == Direction.STRAIGHT.value:
            action = 'w-0'
            # write_read(action)
        elif direction.value == Direction.RIGHT.value:
            action = f'd-{turn_value}'
            # write_read(action)
        elif direction.value == Direction.LEFT.value:
            action = f'a-{turn_value}'
            # write_read(action)

        # cv2.imshow('Mask', mask)
        # cv2.imshow('Frame', frame_with_road_sign)

        key = cv2.waitKey(10) & 0xFF

        if key == ord('q'):
            is_finish = True
            # write_read('r-0')

        (flag, img) = cv2.imencode(".jpg", frame_with_road_sign)
    
        if not flag:
            continue
        
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(img) + b'\r\n')
    

app = Flask(__name__)

@app.route("/")
def index():
    return Response(main(), mimetype = "multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    app.run(host="10.24.224.233", port = 8000, debug = True, threaded = True, use_reloader = False)


