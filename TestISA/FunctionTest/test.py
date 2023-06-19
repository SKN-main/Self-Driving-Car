import numpy as np
import cv2
import os
import v4l2capture
import select

video = v4l2capture.Video_device("/dev/video1")
video.set_format(1920,1080)
video.create_buffers(1)
video.queue_all_buffers()
video.start()
while True:
    select.select((video,), (), ()) # Wait for the device to fill the buffer.
    image_data = video.read_and_queue()

    frame = np.frombuffer(image_data, dtype=np.uint8).reshape(1920,1080,2)
    cv_frame = cv2.imdecode(frame, cv2.COLOR_BAYER_RG2BGR)

    cv2.imshow('frame', frame[:,:,0])
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
video.close()
cv2.destroyAllWindows()