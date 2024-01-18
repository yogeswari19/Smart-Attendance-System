import mail_part
import cv2
import time
import face_recognition
import numpy as np
from datetime import datetime
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from smtplib import SMTP
import csv
import os
import pickle
import try_pickle
import pandas as pd
import mail_part

with open('finaltry.bin', 'rb') as f:
    data = pickle.load(f)

class WebcamStream:
    # initialization method
    def __init__(self, stream_id=0):
        self.stream_id = stream_id  # default is 0 for main camera
        # opening video capture stream
        self.vcap = cv2.VideoCapture(self.stream_id)
        if self.vcap.isOpened() is False:
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)
        fps_input_stream = int(self.vcap.get(5))  # hardware fps
        print("FPS of input stream: {}".format(fps_input_stream))
        # reading a single frame from vcap stream for initializing
        self.grabbed, self.frame = self.vcap.read()
        if self.grabbed is False:
            print('[Exiting] No more frames to read')
            exit(0)
        # self.stopped is initialized to False
        self.stopped = True
        # thread instantiation
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True  # daemon threads run in background

    # method to start thread
    def start(self):
        self.stopped = False
        self.t.start()

    #  method to stop reading frames
    def stop(self):
        self.stopped = True

    # method passed to thread to read next available frame
    def update(self):
        while True:
            if self.stopped is True:
                break
            self.grabbed, self.frame = self.vcap.read()
            if self.grabbed is False:
                print('[Exiting] No more frames to read')
                self.stopped = True
            break
        self.vcap.release()

    # method to return latest read frame
    def read(self):
        return self.frame

# cap = cv2.VideoCapture(0)

webcam_stream = WebcamStream(stream_id=0)  # 0 id for main camera
webcam_stream.start()
# processing frames in input stream
num_frames_processed = 0
start = time.time()
while True:
    if webcam_stream.stopped is True:
        break
    else:
        frame = webcam_stream.read()
        # img = self.frame  # cap.read()
        # img = captureScreen()
        imgs = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
        facescurframe = face_recognition.face_locations(imgs)
        encodescurframe = face_recognition.face_encodings(imgs, facescurframe)

        for encodeFace, faceLoc in zip(encodescurframe, facescurframe):
            matches = face_recognition.compare_faces(data, encodeFace)
            facedis = face_recognition.face_distance(data, encodeFace)
            matchindex = np.argmin(facedis)
            # print(len(matchIndex))

            if matches[matchindex]:
                name = try_pickle.classNames[matchindex]
                print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                # obj.run(name)
                mail_part.writeintocsv(name)
    # adding a delay for simulating video processing time
    delay = 0.03  # delay value in seconds
    time.sleep(delay)
    num_frames_processed += 1
    # displaying frame
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
end = time.time()
webcam_stream.stop()  # stop the webcam stream

# printing time elapsed and fps
elapsed = end - start
fps = num_frames_processed / elapsed
print("FPS: {} , Elapsed Time: {} ".format(fps, elapsed))
# closing all windows
cv2.destroyAllWindows()
