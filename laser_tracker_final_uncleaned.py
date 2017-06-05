import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)
while(1):
    # Take each frame
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([0,0,195])
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
    for i in range (0, len(keypoints)):
        x = keypoints[i].pt[0]
        y = keypoints[i].pt[1]
        print(x,y)
    #print keypoints
    ## Show the image
    #im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    #cv2.imshow('image',im_with_keypoints)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
