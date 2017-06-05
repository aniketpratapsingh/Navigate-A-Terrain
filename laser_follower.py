import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
PWMR = GPIO.PWM(24, 60)
PWMR1 = GPIO.PWM(23, 60)
PWML = GPIO.PWM(27, 60)
PWML1 = GPIO.PWM(22, 60)
PWMR.start(0)
PWMR1.start(0)
PWML.start(0)
PWML1.start(0)
def move_forward():
    print "Going Forward"
    PWMR.ChangeDutyCycle(100)
    #PWMR1.ChangeDutyCycle(0)
    PWML.ChangeDutyCycle(75)
    #PWML1.ChangeDutyCycle(0)
    time.sleep(10)
    PWMR.stop()
    PWML.stop()
def move_backward():
    print "Going Backward"
    #PWMR.ChangeDutyCycle(0)
    PWMR1.ChangeDutyCycle(100)
    #PWML.ChangeDutyCycle(0)
    PWML1.ChangeDutyCycle(75)
    time.sleep(10)
    PWMR1.stop()
    PWML1.stop(),
while(1):
    # Take each frame
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([0,0,230])
    upper_blue = np.array([0,0,255])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    #res = cv2.bitwise_and(frame,frame, mask= mask)
    #res = cv2.medianBlur(res,5)
    cv2.imshow("mask",mask)
    params = cv2.SimpleBlobDetector_Params()
    # Change thresholds
    params.minThreshold = 10;
    params.maxThreshold = 200;
    # Filter by Area.
    params.filterByColor = False
    #params.blobColor = 255
    params.filterByArea = True
    params.minArea = 4
    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.1
    # Filter by Convexity
    params.filterByConvexity = False
    #params.minConvexity = 0.87
    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.01
    # Create a detector with the parameters
    ver = (cv2.__version__).split('.')
    if int(ver[0]) < 3 :
            detector = cv2.SimpleBlobDetector(params)
    else :
            detector = cv2.SimpleBlobDetector_create(params)
            ## Do the processing
    keypoints = detector.detect(mask)
    if keypoints == []:
            PWMR.ChangeDutyCycle(0)
            PWML.ChangeDutyCycle(0)
            PWMR1.ChangeDutyCycle(0)
            PWML1.ChangeDutyCycle(0)
            #send message to nodemcu cant_see_laser
            #mqttc.publish("toNodeMCU","no_laser")
    for i in range (0, len(keypoints)):
            x = keypoints[i].pt[0]
            y = keypoints[i].pt[1]
            print(x,y)
            tan = (240-y)/(160-x)
            angle = math.degrees(math.atan(tan))
            print angle
            if x<120 or x>160 or y<100 or y>140:
                if x<160 and y<240:
                    PWMR1.ChangeDutyCycle(0)
                    PWML1.ChangeDutyCycle(0)
                    PWML.ChangeDutyCycle((97*0.6+int((x)*(97*0.4)/160))/1.5)
                    PWMR.ChangeDutyCycle(100/1.5)
                    print "Calculated PWM"
                    print int((90-angle)*97/90)
                if x>160 and y<240:
                    PWMR1.ChangeDutyCycle(0)
                    PWML1.ChangeDutyCycle(0)
                    PWMR.ChangeDutyCycle((100*0.8+int((x-160)*(100*0.2)/160))/1.5)
                    PWML.ChangeDutyCycle(97/1.5)
                    print "Calculated PWM"
                    print int((90+angle)*97/90)
                '''if x<160 and y>120:
                    PWMR.ChangeDutyCycle(0)
                    PWML.ChangeDutyCycle(0)
                    PWMR1.ChangeDutyCycle((100*0.7+int((-angle)*(100*0.4)/90))/2)
                    PWML1.ChangeDutyCycle(97/2)
                    print "Calculated PWM"
                    print int((90+angle)*97/90)
                if x>160 and y>120:
                    PWMR.ChangeDutyCycle(0)
                    PWML.ChangeDutyCycle(0)
                    PWML1.ChangeDutyCycle((97*0.7+int((angle)*(97*0.4)/90))/2)
                    PWMR1.ChangeDutyCycle(100/2)
                    print "Calculated PWM"
                    print int((90-angle)*97/90)'''
            else:
                PWMR.ChangeDutyCycle(0)
                PWML.ChangeDutyCycle(0)
                PWMR1.ChangeDutyCycle(0)
                PWML1.ChangeDutyCycle(0)
    #print keypoints
    ## Show the image
    #im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    #cv2.imshow('image',im_with_keypoints)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
PWMR.stop()
PWML.stop()
PWMR1.stop()
PWML1.stop()

cv2.destroyAllWindows()
GPIO.cleanup
