from imutils.video import VideoStream
from flask import Response, Flask
import cv2

app = Flask(__name__)


vs = VideoStream(src = "nvarguscamerasrc ! video/x-raw(memory:NVMM), " \
	"width=(int)1280, height=(int)720,format=(string)NV12, " \
	"framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, " \
	"format=(string)BGRx ! videoconvert ! video/x-raw, " \
	"format=(string)BGR ! appsink").start()

@app.route("/")
def index():
    return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")

def generate():
    while True:
        frame = vs.read()
        # frame = cv2.resize(frame, (640, 480))
        (flag, img) = cv2.imencode(".jpg", frame)
       
        if not flag:
            continue

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(img) + b'\r\n')

if __name__ == '__main__':
    # app.run(host="127.0.0.1", port = 8000, debug = True, threaded = True, use_reloader = False)
    app.run(host="10.24.224.221", port = 8000, debug = True, threaded = True, use_reloader = False)

vs.stop()