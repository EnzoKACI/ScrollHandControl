import cv2
import time
import math
import HandTrackingModule as ht
import pyautogui

pyautogui.FAILSAFE = True

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)

# id 3 is width and id 4 is height
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
det = ht.HandDetector(detectionCon=0.8, maxHands=1)

def scrolling(m2b, m2t):
    if m2b is None:
        return None
    elif m2t > 40:
        if m2b > 210:  # distance increased (with margin)
            print("scroll up")
            pyautogui.scroll(75)
        elif m2b < 200:  # distance decreased (with margin)
            print("scroll down")
            pyautogui.scroll(-75)
    elif m2t < 40:
        print("stop scrolling")

while True:
    success, img = cap.read()
    img = det.findHands(img)
    lmList = det.findPosition(img, draw=False)
    if len(lmList) != 0:

        x1, y1 = lmList[12][1], lmList[12][2]  # middle
        x2, y2 = lmList[0][1], lmList[0][2]  # base
        x3, y3 = lmList[4][1], lmList[4][2]  # thumb
        cv2.circle(img, (x1, y1), 7, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x3, y3), 7, (0, 255, 255), cv2.FILLED)

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        middle2base = math.hypot(x2 - x1, y2 - y1)
        cv2.putText(img, str(int(middle2base)), (3, 30), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255, 0, 255), 3)

        cv2.line(img, (x1, y1), (x3, y3), (255, 255, 255), 3)
        middle2thumb = math.hypot(x3 - x1, y3 - y1)
        cv2.putText(img, str(int(middle2thumb)), (3, 60), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255, 255, 255), 3)

        scrolling(middle2base, middle2thumb)


    cTime = time.time()
    fps = 1 // (cTime - pTime)
    pTime = cTime

    # cv2.imshow("Img", img)
    cv2.waitKey(1)
