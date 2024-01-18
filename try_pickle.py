import os
import cv2
import face_recognition
import pickle

path = 'Training_images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):

    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    print(encodeList)
    return encodeList

encodeListKnown = findEncodings(images)
# print('Encoding Complete')

with open('finaltry.bin', 'wb') as f:
    pickle.dump(encodeListKnown, f,pickle.HIGHEST_PROTOCOL)

    # print(type('pickletry.pkl'))
#     str_version = f.decode('unicode_escape')
#     decoded = pickle.loads(str_version.encode('utf-8', 'unicode_escape').replace(b'\xc2', b''))
# print(len(decoded))



