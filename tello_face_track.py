import time
import cv2
import numpy as np
from djitellopy import tello

drone = tello.Tello()
drone.connect()
print(drone.get_battery())
drone.streamon()
drone.takeoff()
drone.send_rc_control(0, 0, 20, 0)
time.sleep(2.2)


#cap = cv2.VideoCapture(0)

w, h = (760, 540)
fbRange = [4200, 4800]
pid = [0.4, 0.4, 0]
pError = 0

def findFace(video):
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    myFaceListC = []
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(video, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cx = x+w//2
        cy = y+h//2
        area = w*h
        cv2.circle(video, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return video, [myFaceListC[i], myFaceListArea[i]]
    else:
        return video, [[0, 0], 0]


def trackFace( info, w, pid, pError):

    area = info[1]
    x,y = info[0]
    fb = 0

    error = x-w//2
    speed = pid[0] * error + pid[1] * (error-pError)
    speed = int(np.clip(speed, -80, 80))

    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20

    #print(speed, fb)

    if x == 0:
        speed = 0
        error = 0

    drone.send_rc_control(0, fb, 0, speed)
    return error

while True:

    video = drone.get_frame_read().frame
    #_, video = cap.read()
    video = cv2.resize(video, (w, h))
    video, info = findFace(video)
    pError = trackFace(info, w, pid, pError)
    #print("Center", info[0], "Area", info[1])
    cv2.imshow("video", video)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        drone.land()
        break
