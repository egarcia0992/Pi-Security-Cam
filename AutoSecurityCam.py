import os
os.environ["LIBCAMERA_LOG_LEVELS"] = "3" # Turn off logs except for ERRORS
import time
import subprocess
from collections import deque
from datetime import datetime
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

picam2 = Picamera2()
video_config = picam2.create_video_configuration(
    main={"size": (640, 480)}) # Set resolution
picam2.configure(video_config)
picam2.set_controls({"FrameRate": 10})
encoder = H264Encoder(1000000) # Set bitrate (2 Mbps bitrate = 2000000)
directory = "/home/pizero/Desktop/Security Cam/Footage"
queue = deque() #FIFO video order queue
# Start recording
while(True):
    timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    filename = f"{directory}/video_{timestamp}.h264"
    queue.append(filename)
    result = subprocess.run(["du", "-s", directory], capture_output=True, text=True)
    result = result.stdout.split('\t')[0]
#     print(result) # 1,048,576 = 1GB
    while int(result) > 20971520:
        os.remove(queue.popleft())
#         print("removed")
        result = subprocess.run(["du", "-s", directory], capture_output=True, text=True)
        result = result.stdout.split('\t')[0]

    picam2.start_recording(encoder, filename)
    time.sleep(600) # In seconds
    picam2.stop_recording()
