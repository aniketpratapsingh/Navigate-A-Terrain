import RPi.GPIO as GPIO
import time
import cv2
import math
import numpy as np
import math
import paho.mqtt.client as mqtt
import threading
from threading import Thread

mqttc = mqtt.Client("", True, None, mqtt.MQTTv31)
# Define Variables
MQTT_BROKER = "192.168.10.1"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "toRPi"

def on_connect(mosq, obj, rc):
	#Subscribe to a the Topic
	mqttc.subscribe(MQTT_TOPIC, 0)

# Define on_subscribe event Handler
def on_subscribe(mosq, obj, mid, granted_qos):
    print "Subscribed to RPi Topic"


cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
PWMR = GPIO.PWM(24, 60)
PWMR1 = GPIO.PWM(23, 60)
PWML = GPIO.PWM(27, 60)
PWML1 = GPIO.PWM(22, 60)
RED = GPIO.PWM(12, 100)
GREEN = GPIO.PWM(16, 100)
BLUE = GPIO.PWM(20, 100)
RED.start(0)
GREEN.start(0)
BLUE.start(0)
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
    PWML1.stop()
def follower():
        global message
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
                params.minArea = 15
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
                        mqttc.publish("toNodeMCU","no_laser")
                for i in range (0, len(keypoints)):
                        x = keypoints[i].pt[0]
                        y = keypoints[i].pt[1]
                        print(x,y)
                        tan = (200-y)/(160-x)
                        angle = math.degrees(math.atan(tan))
                        if angle < 90 and angle >0:
                            PWML.ChangeDutyCycle(int((90-angle)*97/90))
                            PWMR.ChangeDutyCycle(100)
                        if angle > (-90) and angle < 0:
                            PWMR.ChangeDutyCycle(int((90+angle)*100/90))
                            PWML.ChangeDutyCycle(97)
                if(message!="follow"):
                        cv2.destroyAllWindows()
                        break
                
                '''PWMR.ChangeDutyCycle(0)
                PWML.ChangeDutyCycle(0)
                PWMR1.ChangeDutyCycle(0)
                PWML1.ChangeDutyCycle(0)
                if y>210 and x<70:
                    #left backwards
                    PWMR.ChangeDutyCycle(100)
                    PWML.ChangeDutyCycle(92)
                elif y>210 and x>170:
                    #right backwards
                    #PWMR.ChangeDutyCycle(100)
                    #PWML.ChangeDutyCycle(96)
                elif y>210:
                    #backwards
                    PWMR.ChangeDutyCycle(100)
                    PWML.ChangeDutyCycle(96)
                elif y<110 and x<70:
                    #left forward

                elif y<110 and x>170:
                    #right forward
                elif y<210:
                    #forward
                    PWMR1.ChangeDutyCycle(100)
                    PWML1.ChangeDutyCycle(92)

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
                PWMl1.stop()

                cv2.destroyAllWindows()
                GPIO.cleanup'''
def turn_around():
    PWMR.ChangeDutyCycle(100)
    PWML1.ChangeDutyCycle(100)
    time.sleep(2)
    PWMR.ChangeDutyCycle(0)
    PWML1.ChangeDutyCycle(0)

def detect_checkpoint():
    ret, img = cap.read()
    img = img[:,40:280,:]
    ## Do the processing
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    cv2.imshow('thersh',thresh)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    l= len(contours)
    for i in range(0,l):
        
        if(cv2.arcLength(contours[i],True)>50 and cv2.arcLength(contours[i],True)<800 and cv2.contourArea(contours[i]) > 2000 and cv2.contourArea(contours[i])<12000 ):
            print "Area = ",i, cv2.contourArea(contours[i])
            #for i in range(0,l):
            #   if cv2.contourArea(contours[i]) > 2000:# and cv2.contourArea(contours[i])<2000:
            cv2.drawContours(img,contours[i],-1,(0,255,0),3)
            l= len(contours)
            for i in range(0,l):
                    if(cv2.arcLength(contours[i],True)>50 and cv2.arcLength(contours[i],True)<800 and cv2.contourArea(contours[i]) > 2000 and cv2.contourArea(contours[i])<12000 ):
                            print "Area = ",i, cv2.contourArea(contours[i])
                            M = cv2.moments(contours[i])
                            cx = int(M['m10']/M['m00'])
                            cy = int(M['m01']/M['m00'])
                            print "Centroid = ", cx, ", ", cy
                            cv2.circle(img,(cx,cy), 5, (0,0,255), -1)
            ############################################
            r,g,b = img[cx,cy,:]
            RED.ChangeDutyCycle(r*100/255)
            GREEN.ChangeDutyCycle(g*100/255)
            BLUE.ChangeDutyCycle(b*100/255)
            r = str(r)
            g = str(g)
            b = str(b)
            print img[cx,cy,:]
            
            mqttc.publish("toNodeMCU","Color"+r+g+b)
    ############################################
    ## Show the image
    
    cv2.imshow('checkpoint',img)
    #if(cx):
            #break

def stop():
    PWMR.ChangeDutyCycle(0)
    PWML.ChangeDutyCycle(0)
    PWMR1.ChangeDutyCycle(0)
    PWML1.ChangeDutyCycle(0)
message=""

def on_message(mosq, obj, msg):
        global message
        message = msg.payload
        print message
def mqtt_subscriber():
        # Register Event Handlers
        mqttc.on_message = on_message
        mqttc.on_connect = on_connect
        mqttc.on_subscribe = on_subscribe

        # Connect with MQTT Broker
        mqttc.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL )

        # Continue the network loop
        mqttc.loop_forever()
def executer():
        while(1):
                global message
                print message
                if(message=="follow"):
                        follower()
                elif(message=="stop"):
                        stop()
                elif(message=="detect_checkpoint"):
                        detect_checkpoint()
                elif(message=="turn_around"):
                        turn_around()

if __name__=='__main__':
     if __name__ == '__main__':
          Thread(target = mqtt_subscriber).start()
          Thread(target = executer).start()

     '''PWMR.stop()
     PWML.stop()
     PWMR1.stop()
     PWML1.stop()
     RED.stop()
     GREEN.stop()
     BLUE.stop()

     cv2.destroyAllWindows()
     GPIO.cleanup'''
