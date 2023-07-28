import cv2
import numpy as np
import serial
import time

face_cascade = cv2.CascadeClassifier('C:/facetracking/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('C:/facetracking/haarcascade_eye.xml')
margin_x = 80
margin_y = 90

_pan = pan = 75
_tilt = tilt = 75

sp  = serial.Serial('COM3', 9600, timeout=1)

pan = _pan = 75
tilt = _tilt = 75

def send_pan(pan):
    tx_dat = "pan" + str(pan) + "\n"
    sp.write(tx_dat.encode())
    print(tx_dat)

def send_tilt(tilt):
    tx_dat = "tilt" + str(tilt) + "\n"
    sp.write(tx_dat.encode())
    print(tx_dat)

def main(args=None):
    global pan; global _pan; global tilt; global _tilt;
    send_pan(75)
    send_tilt(75)

cap = cv2.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 10)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        face_contour=[(x,y),(x+w,y),(x+w,y+h),(x,y+h)]
        center_x = x + w//2
        center_y = y + h//2
        print("center: ( %s, %s )"%(center_x, center_y)) 
        cv2.drawContours(frame, [np.array(face_contour)], 0, (0, 0, 255), 2)
        roi_gray = gray[y : y + h, x : x + w]
        roi_color = frame[y : y + h, x : x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
        if center_y <= 240-margin_y: # need tilt up 
            if tilt - 1 >= 0:
                tilt = tilt - 1
                send_tilt(tilt); _tilt = tilt
            else:
                tilt = 0
                send_tilt(tilt); _tilt = tilt
        elif center_y < 240+margin_y: # do not change tilt value
            tilt = _tilt
            send_tilt(tilt); _tilt = tilt
        else: # need tilt right
                if tilt + 1 <= 180:
                    tilt = tilt + 1
                    send_tilt(tilt); _tilt = tilt
                else:
                    tilt = 180
                    send_tilt(tilt); _tilt = tilt
        if center_x >= 500-margin_x: # need pan left 
            if pan - 1 >= 0:
                pan = pan - 1
                send_pan(pan); _pan = pan
            else:
                pan = 0
                send_pan(pan); _pan = pan
        elif center_x > 320+margin_x: # do not change tilt value
            pan = _pan
            send_pan(pan); _pan = pan
        else: # need pan right
                if pan + 1 <= 180:
                    pan = pan + 1
                    send_pan(pan); _pan = pan
                else:
                    pan = 180
                    send_pan(pan); _pan = pan     
    cv2.imshow('Videoframe', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()



