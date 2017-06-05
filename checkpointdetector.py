
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)

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
    cap.release()
    cv2.destroyAllWindows()
    return color
detect_checkpoint()
