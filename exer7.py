import cv2
import numpy as np

cap = cv2.VideoCapture('pessoas.mp4')

mog = cv2.createBackgroundSubtractorMOG2(history=300, varThreshold=10, detectShadows=True)

while(cap.isOpened()):
    ret, frame = cap.read()

    fgmask = mog.apply(frame)

    cv2.imshow('frame movimento', fgmask)
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
