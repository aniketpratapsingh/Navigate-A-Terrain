import cv2
cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)
while(1):
    ret, img = cap.read()
    img = img[:,40:280,:]
    ## Do the processing
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
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
            print img[cx,cy,:]
            '''r,g,b = img[cx,cy,:]
            RED.ChangeDutyCycle(r*100/255)
            GREEN.ChangeDutyCycle(g*100/255)
            BLUE.ChangeDutyCycle(b*100/255)
            r = str(r)
            g = str(g)
            b = str(b)
            print img[cx,cy,:]
            
            mqttc.publish("toNodeMCU","Color"+r+g+b)'''
    ############################################
    ## Show the image

    cv2.imshow('checkpoint',img)
    #if(cx):
            #break
