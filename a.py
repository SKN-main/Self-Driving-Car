import cv2

cam=cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), " \
	"width=(int)1280, height=(int)720,format=(string)NV12, " \
	"framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, " \
	"format=(string)BGRx ! videoconvert ! video/x-raw, " \
	"format=(string)BGR ! appsink", cv2.CAP_GSTREAMER)
if cam.isOpened():
	cv2.namedWindow("demo", cv2.WINDOW_AUTOSIZE)
	while True:
		ret_val, img = cam.read();
		if not ret_val:
			break
		cv2.imshow('demo',img)
		if cv2.waitKey(1) == ord('q'):
			break
else:
	print ("camera open failed")