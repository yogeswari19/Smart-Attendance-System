import cv2
import face_recognition
import numpy as np
import threading
import pickle
import try_pickle
import mail_part
import sys
import pandas as pd

if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")

stream_id = 0
camname1 = 'cam1'
camname2 = 'cam2'

with open('finaltry.bin', 'rb') as f:
    data = pickle.load(f)


class WebcamStream(threading.Thread):
    def _init_(self, streaming_id, cname):
        threading.Thread._init_(self)
        self.stream_id = streaming_id  # default is 0 for main camera
        self.cname = cname

    def campreview(self, streaming_id, cname):
        vcap = cv2.VideoCapture(streaming_id)
        while True:
            grabbed, frame = vcap.read()
            while not grabbed:
                vcap.release()
                vcap = cv2.VideoCapture(streaming_id)
                grabbed, frame = vcap.read()
                imgs = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
                imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

                facescurframe = face_recognition.face_locations(imgs)
                encodescurframe = face_recognition.face_encodings(imgs, facescurframe)
                for encodeFace, faceLoc in zip(encodescurframe, facescurframe):
                    matches = face_recognition.compare_faces(data, encodeFace)
                    facedis = face_recognition.face_distance(data, encodeFace)
                    matchindex = np.argmin(facedis)
                    if matches[matchindex]:
                        name = try_pickle.classNames[matchindex]
                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                        cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        cv2.imshow('Face Recognition' + cname, frame)
                        key = cv2.waitKey(5)
                        if key == ord('q'):
                            break
                        status = mail_part.writeintocsv(name)
                        if status:
                            df = pd.read_csv("face_recognition.csv")
                            df['mail details'] = "mail sent"


obj = WebcamStream()

# webcam_stream = WebcamStream(target=obj.campreview, args=(stream_id, camname1))
webcam_stream = WebcamStream(target=obj.campreview, args=(stream_id, camname1))  # 0 id for main camera
webcam_stream.start()

webcam_stream2 = WebcamStream(target=obj.campreview, args=(stream_id, camname2))
webcam_stream2.start()
