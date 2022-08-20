import cv2 as cv
import argparse
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import time
import random
from threading import Thread

low = AudioSegment.from_wav("C:/Users/fneus/PycharmProjects/antilagsound/low.wav")
high = AudioSegment.from_wav("C:/Users/fneus/PycharmProjects/antilagsound/high.wav")

def taskhigh():
    play(high)
    time.sleep(random.uniform(0.6, 2))

def tasklow():
    play(low)
    time.sleep(random.uniform(0.6, 4))

def play_sound():
    t1 = Thread(target=tasklow)
    t2 = Thread(target=tasklow)
    t3 = Thread(target=tasklow)
    t4 = Thread(target=tasklow)
    t5 = Thread(target=tasklow)
    t1.start()
    time.sleep(0.05)
    t2.start()
    time.sleep(0.06)
    t3.start()
    time.sleep(0.03)
    t4.start()
    time.sleep(2)


cap = cv.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)

scale=300

cy = 1
cx = 1

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

charge_time = 0

while True:
    ret, frame = cap.read()
    # frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)

    height, width, channels = frame.shape

    # prepare the crop
    centerX, centerY = int(height / 2), int(width / 2)
    radiusX, radiusY = int(scale * height / 100), int(scale * width / 100)

    minX, maxX = centerX - radiusX, centerX + radiusX
    minY, maxY = centerY - radiusY, centerY + radiusY

    cropped = frame[minX:maxX, minY:maxY]
    frame = cv.resize(cropped, (width, height))

    hls = cv.cvtColor(frame, cv.COLOR_BGR2HLS)  # convert
    h, l, s = cv.split(hls)  # split to h s v



    #h = h * 2.5
    #frame = cv.merge([h,l,s])
    #frame = cv.cvtColor(frame, cv.COLOR_HSV2BGR)

    h = cv.GaussianBlur(h, (5, 5), cv.BORDER_DEFAULT)
    l = cv.GaussianBlur(l, (5, 5), cv.BORDER_DEFAULT)
    k = (cv.inRange(l, 35, 210))

    mask = cv.inRange(h, 65, 81)

    k = k.clip(0, 255)
    k = cv.GaussianBlur(k, (5, 5), cv.BORDER_DEFAULT)
    k = (cv.inRange(k, 250, 255))

    s = cv.inRange(s,60,200)
    s = s.clip(0, 1)

    s = cv.GaussianBlur(s, (7, 7), cv.BORDER_DEFAULT)
    s = cv.inRange(s, 0.9, 1)

    out = (k/255)*mask*(s/255)
    out = out.clip(0,1)

    out = cv.GaussianBlur(out, (11, 11), cv.BORDER_DEFAULT)

    out = cv.inRange(out, 0.9, 2)

    cv.imshow('Input', frame)
    #cv.imshow('mask',mask)
    #cv.imshow('masdsk', k)

    #cv.imshow('Output',out)

    M = cv.moments(out)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

    cv.circle(out, (cx, cy), 7, (100, 100, 100), -1)
    cv.putText(out, "center", (cx - 20, cy - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 2)
    print(f"x: {cx} y: {cy}")
    if cx > 100:    #charge
        charge_time += 1
        print(charge_time)
    if cx < 100:    #discharge
        if charge_time > 10:
            play_thread = Thread(target=play_sound)
            play_thread.start()
            charge_time = 0






    cv.imshow('Ouasdatput', out)

    c = cv.waitKey(1)
    if c == 27:
        break

cap.release()
cv.destroyAllWindows()
