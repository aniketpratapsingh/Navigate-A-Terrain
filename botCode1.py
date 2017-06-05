import RPi.GPIO as GPIO
import time
import cv2
import math
import numpy as np
import math
import paho.mqtt.client as mqtt
import threading
from threading import Thread
import rgbled as rgb

cap = cv2.VideoCapture(0)

cap.set(3,320)
cap.set(4,240)

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
                    tan = (120-y)/(160-x)
                    angle = math.degrees(math.atan(tan))
                    print angle
                    if x<120 or x>160 or y<100 or y>140:
                        if x<160 and y<120:
                            PWMR1.ChangeDutyCycle(0)
                            PWML1.ChangeDutyCycle(0)
                            PWML.ChangeDutyCycle((97*0.7+int((angle)*(97*0.5)/90))/1.5)
                            PWMR.ChangeDutyCycle(100/1.5)
                            print "Calculated PWM"
                            print int((90-angle)*97/90)
                        if x>160 and y<120:
                            PWMR1.ChangeDutyCycle(0)
                            PWML1.ChangeDutyCycle(0)
                            PWMR.ChangeDutyCycle((100*0.7+int((-angle)*(100*0.5)/90))/1.5)
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
                if(message!="follow"):
                        cap.release()
                        cv2.destroyAllWindows()
                        break
def turn_around():
    PWMR.ChangeDutyCycle(100)
    PWML1.ChangeDutyCycle(100)
    time.sleep(2)
    PWMR.ChangeDutyCycle(0)
    PWML1.ChangeDutyCycle(0)

def detect_checkpoint():
        
        while(1):
                ret, img = cap.read()
                img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
                lower = np.array([0,226,183])
                upper = np.array([45,255,255])
                mask = cv2.inRange(img_hsv,lower,upper)
                img_result = cv2.bitwise_and(img,img,mask=mask)
                
                gray = cv2.cvtColor(img_result,cv2.COLOR_BGR2GRAY)
                ret,thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)
                contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                l= len(contours)
                if l > 0:
                    color="red"
                    print "red"
                    break
                
                lower = np.array([130,91,255])
                upper = np.array([177,255,255])
                mask = cv2.inRange(img_hsv,lower,upper)
                
                img_result = cv2.bitwise_and(img,img,mask=mask)
                
                gray = cv2.cvtColor(img_result,cv2.COLOR_BGR2GRAY)
                ret,thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)
                contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                l= len(contours)
                if l > 0:
                    color="pink"
                    print "pink"
                    break
                lower = np.array([51,153,100])
                upper = np.array([65,255,255])
                mask = cv2.inRange(img_hsv,lower,upper)
                
                img_result = cv2.bitwise_and(img,img,mask=mask)
                
                gray = cv2.cvtColor(img_result,cv2.COLOR_BGR2GRAY)
                ret,thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)
                contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                l= len(contours)
                if l > 0:
                    color="green"
                    print "green"
                    break
                lower = np.array([135,125,125])
                upper = np.array([155,255,255])
                mask = cv2.inRange(img_hsv,lower,upper)
                
                img_result = cv2.bitwise_and(img,img,mask=mask)
                
                gray = cv2.cvtColor(img_result,cv2.COLOR_BGR2GRAY)
                ret,thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)
                contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                l= len(contours)
                if l > 0:
                    color="blue"
                    print "blue"
                    break
                lower = np.array([106,115,189])
                upper = np.array([118,255,255])
                mask = cv2.inRange(img_hsv,lower,upper)
                
                img_result = cv2.bitwise_and(img,img,mask=mask)
                
                gray = cv2.cvtColor(img_result,cv2.COLOR_BGR2GRAY)
                ret,thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)
                contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                l= len(contours)
                if l > 0:
                    print "sky-blue"
                    color="sky-blue"
                    break
                lower = np.array([30,66,123])
                upper = np.array([56,255,255])
                mask = cv2.inRange(img_hsv,lower,upper)
                
                img_result = cv2.bitwise_and(img,img,mask=mask)
                
                gray = cv2.cvtColor(img_result,cv2.COLOR_BGR2GRAY)
                ret,thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)
                contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                l= len(contours)
                if l > 0:
                    color="yellow"
                    print "yellow"
                    break
        mqttc.publish("toNodeMCU",color)
        if color == "red":
                rgb.redOn()
                time.sleep(5)
                rgb.redOff()
        elif color == "green":
                rgb.greenOn()
                time.sleep(5)
                rgb.greenOff()
        elif color == "blue":
                rgb.blueOn()
                time.sleep(5)
                rgb.blueOff()
        elif color == "yellow":
                rgb.yellowOn()
                time.sleep(5)
                rgb.yellowOff()
        elif color == "sky-blue":
                rgb.skyblueOn()
                time.sleep(5)
                rgb.skyblueOff()
        elif color == "pink":
                rgb.pinkOn()
                time.sleep(5)
                rgb.pinkOff()
        elif color == "white":
                rgb.whiteOn()
                time.sleep(5)
                rgb.whiteOff()
        global message
        message = ""
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
