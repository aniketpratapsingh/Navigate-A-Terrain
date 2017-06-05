## Please make sure your USB camera is connected to the RPi before running this program.

import cv2
import numpy as np

capture = cv2.VideoCapture(0)
capture.set(3,320)
capture.set(4,240)
while cv2.waitKey(1) != 27:
    ## 27 is the ASCII value of ESC.
    ## Pressing ESC will exit the program.
    flag, frame = capture.read()
    cv2.imshow('frame', frame)

cv2.destroyAllWindows()
## The frame window may become unresponsive at times. Don't worry, it is not a programming error.
## Close the 'frame' window or close the python shell manually to exit.
