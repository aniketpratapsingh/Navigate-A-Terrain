'''
*Team Id : 2317
*Author List : Aniket Pratap Singh
*Filename: section1.py
*Theme: NT-eYRC
*Functions: sine(angle), cosine(angle), readImage(filePath), findNeighbours(img, level, cellnum, size), colourCell(img, level, cellnum, size, colourVal), buildGraph(img,size), findStartPoint(img,size), findPath(graph,start,end,path=[])
*Global Variables: None
'''
import paho.mqtt.client as mqtt
import threading
from threading import Thread
# Define Variables
mqttc = mqtt.Client("", True, None, mqtt.MQTTv31)

MQTT_BROKER = "192.168.10.1"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "toNodeMCU"
MQTT_MSG = "Hello MQTT"
message=""
def on_subscribe(mosq, obj, mid, granted_qos):
    print "Subscribed to Laptop Topic"

# Define on_connect event Handler
def on_connect(mosq, obj, rc):
	print "Connected to MQTT Broker"
	mqttc.subscribe("Laptop",0)

# Define on_publish event Handler
def on_publish(client, userdata, mid):
	print "Message Published..."
import numpy as np
import cv2
import math
import time

'''
*Function Name: sine
*Input: angle->angle in degrees
*Output: sine of the angle.
*Logic: using the math library function to give sine of the angle.
*Example Call: sine(60)
'''
##  Returns sine of an angle.
def sine(angle):
    return math.sin(math.radians(angle))

'''
*Function Name: cosine
*Input: angle->angle in degrees
*Output: cosine of the angle.
*Logic: using the math library function to give cosine of the angle.
*Example Call: cosine(60)
'''
##  Returns cosine of an angle
def cosine(angle):
    return math.cos(math.radians(angle))

'''
*Function Name: readImage
*Input: filePath->address of the file on the hard disk
*Output: Binary image of the file located at the address location.
*Logic: Reads an image from the specified filepath and converts it to Grayscale. Then applies binary thresholding to the image.
*Example Call: readImage("image_09.jpg")
'''
##  Reads an image from the specified filepath and converts it to Grayscale. Then applies binary thresholding
##  to the image.
def readImage(filePath):
    mazeImg = cv2.imread(filePath)
    grayImg = cv2.cvtColor(mazeImg, cv2.COLOR_BGR2GRAY)
    ret,binaryImage = cv2.threshold(grayImg,127,255,cv2.THRESH_BINARY)
    return binaryImage


'''
*Function Name: findNeighbours
*Input: img->image matrix, level->level of the cell, cellnum->cell number of the cell, size-> size flag of the image.
*Output: The list of cells which are traversable from the specified cell.
*Logic: The walls are detected by increasing and decreasing level and cellnum by 0.5
*Example Call: findNeighbours(img, 6, 5, 1)
'''
##  This function accepts the img, level and cell number of a particular cell and the size of the maze as input
##  arguments and returns the list of cells which are traversable from the specified cell.
def findNeighbours(img, level, cellnum):
    neighbours = []
    ############################# Add your Code Here ###############################
    s = 495
    if level == 1:
        t = 360/4
        l = 4
    elif level == 2:
        t = 360/10                                                                      #t is the step angle
        l = 10                                                                       #l is the last cellnum for the level
    elif level == 3:
        t = 360/15
        l = 15
    elif level == 4:
        t = 360/20
        l = 20
    if level == 0 and cellnum == 0:
        neighbours.append((1,4))
        #for the centre of the maze
        #for i in range(1,4):
            #if(img[s + 40*sine(60*(i-0.5)-90),s + 40*cosine(60*(i-0.5)-90)] > 127):
                #neighbours.append((level+1,i))
    else:
        if cellnum == 1:                                                                                    #if the cellnum is 1 then it will go to last cellnum
            neighbours.append((level,l))
        else:
            neighbours.append((level,cellnum-1))
        if cellnum == l:
            neighbours.append((level,1))
        else:
            neighbours.append((level,cellnum+1))
        '''if(img[s + 40*(level+0.5)*sine(t*(cellnum-1)-90),s + 40*(level+0.5)*cosine(t*(cellnum-1)-90)] > 127):         #for the previous cellnum
            if cellnum == 1:                                                                                    #if the cellnum is 1 then it will go to last cellnum
                neighbours.append((level,l))
            else:
                neighbours.append((level,cellnum-1))


        if(img[s + 40*(level+0.5)*(sine(t*cellnum)-90),s + 40*(level+0.5)*(cosine(t*cellnum)-90)] > 127):                 #for the next cellnum
            if cellnum == l:
                neighbours.append((level,1))
            else:
                neighbours.append((level,cellnum+1))


        if level == 3 or level == 4:                                                                            #for level 3,4 the jump to next level is from 1 cell to 1 cell
            if(img[s + 40*(level+1)*sine(t*(cellnum-0.5)),s + 40*(level+1)*cosine(t*(cellnum-0.5))] > 127):
                neighbours.append((level+1,cellnum))
        elif level == 1 or level == 2 or level == 5:                                                            #for level 1,2,5 the jump to next level is from 1 cell to 2 cells
            if(img[s + 40*(level+1)*sine(t*(cellnum-0.25)),s + 40*(level+1)*cosine(t*(cellnum-0.25))] > 127):
                neighbours.append((level+1,2*cellnum))
            if(img[s + 40*(level+1)*sine(t*(cellnum-0.75)),s + 40*(level+1)*cosine(t*(cellnum-0.75))] > 127):
                neighbours.append((level+1,2*cellnum-1))

        if level == 6 or level == 3 or level == 2 :                                                             #for level 2,3,6 the jump to previous level is from 2 cells to 1 cell
            if(img[s + 40*level*sine(t*(cellnum-0.5)),s + 40*level*cosine(t*(cellnum-0.5))] > 127):
                neighbours.append((level-1,(cellnum+1)/2))
        elif level == 4 or level ==5:                                                                           #for level 4,5 the jump to previous level is from 1 cell to 1 cell
            if(img[s + 40*level*sine(t*(cellnum-0.5)),s + 40*level*cosine(t*(cellnum-0.5))] > 127):
                neighbours.append((level-1,cellnum))
        elif level == 1 :                                                                                       #for level 1 the jump to next level is to (0,0)
            if(img[s + 40*level*sine(t*(cellnum-0.5)),s + 40*level*cosine(t*(cellnum-0.5))] > 127):
                neighbours.append((0,0))'''
        #if(img[s + (100*(level)-23)*sine(t*((l+1-cellnum)-0.5)-90),s + (100*(level)-23)*cosine(t*((l+1-cellnum)-0.5)-90)] > 127):
            #print level,cellnum
            #print s + (100*(level)-23)*sine(t*((l+1-cellnum)-0.5)-90),s + (100*(level)-23)*cosine(t*((l+1-cellnum)-0.5)-90)
        if level == 1:
            if cellnum == 1:
                a,b = 1,3
                if(img[456,456] < 127):
                    neighbours.append((0,0))
            elif cellnum == 2:
                a,b = 3,5
                if(img[540,456] < 127):
                    neighbours.append((0,0))
            elif cellnum == 3:
                a,b = 6,8
                if(img[534,534] < 127):
                    neighbours.append((0,0))
            elif cellnum == 4:
                a,b = 8,10
                if(img[450,535] < 127):
                    neighbours.append((0,0))

            for p in range(a,b+1):
                if(img[s + 177*sine((360/10)*((10+1-p)-0.5)-90),s + 177*cosine((360/10)*((10+1-p)-0.5)-90)] > 127):
                    neighbours.append((level+1,p))
        if level == 2:
            if (img[s + 177*sine(t*((l+1-cellnum)-0.5)-90),s + 177*cosine(t*((l+1-cellnum)-0.5)-90)] > 127):
                #print level,cellnum
                #print s + (100*(level)-23)*sine(t*((l+1-cellnum)-0.5)-90),s + (100*(level)-23)*cosine(t*((l+1-cellnum)-0.5)-90)
                if cellnum == 1 or cellnum == 2 or cellnum == 3 :
                    neighbours.append((level-1,1))
                if cellnum == 3 or cellnum == 4 or cellnum == 5 :
                    neighbours.append((level-1,2))
                if cellnum == 6 or cellnum == 7 or cellnum == 8 :
                    neighbours.append((level-1,3))
                if cellnum == 8 or cellnum == 9 or cellnum == 10 :
                    neighbours.append((level-1,4))

            if cellnum == 1:
                a,b = 1,2
            elif cellnum == 2:
                a,b = 2,3
                #print a,b
            elif cellnum == 3:
                a,b = 4,5
            elif cellnum == 4:
                a,b = 5,6
            elif cellnum == 5:
                a,b = 7,8
            elif cellnum == 6:
                a,b = 8,9
            elif cellnum == 7:
                a,b = 10,11
            elif cellnum == 8:
                a,b = 11,12
            elif cellnum == 9:
                a,b = 13,14
            elif cellnum == 10:
                a,b = 14,15
            for p in range(a,b+1):
                if(img[s + 276*sine((360/15)*((15+1-p)-0.5)-90),s + 276*cosine((360/15)*((15+1-p)-0.5)-90)] > 127):
                    neighbours.append((level+1,p))
                    #print level,p
        if level == 3:
            if(img[s + 276*sine(t*((l+1-cellnum)-0.5)-90),s + 276*cosine(t*((l+1-cellnum)-0.5)-90)] > 127):
                #print level,cellnum
                #print s + (100*(level)-23)*sine(t*((l+1-cellnum)-0.5)-90),s + (100*(level)-23)*cosine(t*((l+1-cellnum)-0.5)-90)
                if cellnum == 1 or cellnum == 2:
                    neighbours.append((level-1,1))
                if cellnum == 2 or cellnum == 3:
                    neighbours.append((level-1,2))
                if cellnum == 4 or cellnum == 5:
                    neighbours.append((level-1,3))
                if cellnum == 5 or cellnum == 6:
                    neighbours.append((level-1,4))
                if cellnum == 7 or cellnum == 8:
                    neighbours.append((level-1,5))
                if cellnum == 8 or cellnum == 9:
                    neighbours.append((level-1,6))
                if cellnum == 10 or cellnum == 11:
                    neighbours.append((level-1,7))
                if cellnum == 11 or cellnum == 12:
                    neighbours.append((level-1,8))
                if cellnum == 13 or cellnum == 14:
                    neighbours.append((level-1,9))
                if cellnum == 14 or cellnum == 15:
                    neighbours.append((level-1,10))

            if cellnum == 1:
                a,b = 1,2
            elif cellnum == 2:
                a,b = 2,3
                #print a,b
            elif cellnum == 3:
                a,b = 3,4
            elif cellnum == 4:
                a,b = 5,6
            elif cellnum == 5:
                a,b = 6,7
            elif cellnum == 6:
                a,b = 7,8
            elif cellnum == 7:
                a,b = 9,10
            elif cellnum == 8:
                a,b = 10,11
            elif cellnum == 9:
                a,b = 11,12
            elif cellnum == 10:
                a,b = 13,14
            elif cellnum == 11:
                a,b = 14,15
            elif cellnum == 12:
                a,b = 15,16
            elif cellnum == 13:
                a,b = 17,18
            elif cellnum == 14:
                a,b = 18,19
            elif cellnum == 15:
                a,b = 19,20
            for p in range(a,b+1):
                if(img[s + 374*sine((360/20)*((20+1-p)-0.5)-90),s + 374*cosine((360/20)*((20+1-p)-0.5)-90)] > 127):
                    neighbours.append((level+1,p))
                    #print level,p
        if level == 4:
            if(img[s + 374*sine(t*((l+1-cellnum)-0.5)-90),s + 374*cosine(t*((l+1-cellnum)-0.5)-90)] > 127):
                #print level,cellnum
                #print s + (100*(level)-23)*sine(t*((l+1-cellnum)-0.5)-90),s + (100*(level)-23)*cosine(t*((l+1-cellnum)-0.5)-90)
                if cellnum == 1 or cellnum == 2:
                    neighbours.append((level-1,1))
                if cellnum == 2 or cellnum == 3:
                    neighbours.append((level-1,2))
                if cellnum == 3 or cellnum == 4:
                    neighbours.append((level-1,3))
                if cellnum == 5 or cellnum == 6:
                    neighbours.append((level-1,4))
                if cellnum == 6 or cellnum == 7:
                    neighbours.append((level-1,5))
                if cellnum == 7 or cellnum == 8:
                    neighbours.append((level-1,6))
                if cellnum == 9 or cellnum == 10:
                    neighbours.append((level-1,7))
                if cellnum == 10 or cellnum == 11:
                    neighbours.append((level-1,8))
                if cellnum == 11 or cellnum == 12:
                    neighbours.append((level-1,9))
                if cellnum == 13 or cellnum == 14:
                    neighbours.append((level-1,10))
                if cellnum == 14 or cellnum == 15:
                    neighbours.append((level-1,11))
                if cellnum == 15 or cellnum == 16:
                    neighbours.append((level-1,12))
                if cellnum == 17 or cellnum == 18:
                    neighbours.append((level-1,13))
                if cellnum == 18 or cellnum == 19:
                    neighbours.append((level-1,14))
                if cellnum == 19 or cellnum == 20:
                    neighbours.append((level-1,15))


    #################################################################################
    return neighbours

def findMarkers(img):             ## You can pass your own arguments in this space.
    list_of_markers = []
    ############################# Add your Code Here ################################

    for level in range(1,5):
        if level == 1:
            for cellnum in range(1,5):
                b = np.arange(cellnum+0.2, cellnum-0.2+1,0.1)
                a = np.arange(78+100*(level-1)+10,78+100*(level)-10,0.1)
                for l in a:
                    for c in b:
                        if(img[495 + (l)*sine((360/4)*((4+1-c))-90),495 + (l)*cosine((360/4)*((4+1-c))-90)] < 127):
                            list_of_markers.append((level,cellnum))
                            break
                    else:
                        continue
                    break

        if level == 2:
            for cellnum in range(1,11):
                b = np.arange(cellnum+0.2, cellnum-0.2+1,0.1)
                a = np.arange(78+100*(level-1)+10,78+100*(level)-10,0.1)
                for l in a:
                    for c in b:
                        if(img[495 + (l)*sine((360/10)*((10+1-c))-90),495 + (l)*cosine((360/10)*((10+1-c))-90)] < 127):
                            list_of_markers.append((level,cellnum))
                            break
                    else:
                        continue
                    break
        if level == 3:
            for cellnum in range(1,16):
                b = np.arange(cellnum+0.2, cellnum-0.2+1,0.1)
                a = np.arange(78+100*(level-1)+10,78+100*(level)-10,0.1)
                for l in a:
                    for c in b:
                        if(img[495 + (l)*sine((360/15)*((15+1-c))-90),495 + (l)*cosine((360/15)*((15+1-c))-90)] < 127):
                            list_of_markers.append((level,cellnum))
                            break
                    else:
                        continue
                    break
        if level == 4:
            for cellnum in range(1,21):
                if cellnum == 1:
                    b = np.arange(cellnum+0.5, cellnum-0.2+1,0.1)
                    a = np.arange(78+100*(level-1)+45,78+100*(level)-30,0.1)
                    for l in a:
                        for c in b:
                            if(img[495 + (l)*sine((360/20)*((20+1-c))-90),495 + (l)*cosine((360/20)*((20+1-c))-90)] < 127):
                                list_of_markers.append((level,cellnum))
                                break
                        else:
                            continue
                        break
                elif cellnum == 20:
                    b = np.arange(cellnum+0.2, cellnum-0.5+1,0.1)
                    a = np.arange(78+100*(level-1)+10,78+100*(level)-10,0.1)
                    for l in a:
                        for c in b:
                            if(img[495 + (l)*sine((360/20)*((20+1-c))-90),495 + (l)*cosine((360/20)*((20+1-c))-90)] < 127):
                                list_of_markers.append((level,cellnum))
                                break
                        else:
                            continue
                        break
                else:
                    b = np.arange(cellnum+0.2, cellnum-0.2+1,0.1)
                    a = np.arange(78+100*(level-1)+10,78+100*(level)-10,0.1)
                    for l in a:
                        for c in b:
                            if(img[495 + (l)*sine((360/20)*((20+1-c))-90),495 + (l)*cosine((360/20)*((20+1-c))-90)] < 127):
                                list_of_markers.append((level,cellnum))
                                break
                        else:
                            continue
                        break

    #################################################################################
    return list_of_markers
def findOptimumPath(img,markers):     ## You can pass your own arguments in this space.
    path_array = []
    #############  Add your Code here   ###############
    initial_point =(4,1)
    final_point = (0,0)
    graph = buildGraph(img)               ##Building the graph using the funtion.
    start = initial_point
    while(start != final_point):
        shortest = []
        if(markers==[]):                                            ##Finding the shortest path from start point to one of the markers
            shortest = findPath(graph, start, final_point)
            start = final_point
        for coords in markers:
            newpath = findPath(graph, start, coords)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
        l = len(shortest)
        start = shortest[l-1]                                       ##Set last point of shortest path as start point for next shortest path.
        l2 = len(markers)
        temp = markers
        for i in range(0,l2):                                       ##Deleting the last point of shortest path from markers.
            if(temp[i]==start):
                del markers[i]
                break
        path_array.append(shortest)                                 ##Adding the shortest path to the Path Array.
    ###################################################
    return path_array
'''
*Function Name: colourCell
*Input: img->image matrix, level->level of the cell, cellnum->cell number of the cell, size-> size flag of the image, colourVal-> the intensity of the colour
*Output: The image with the painted cell.
*Logic: using trignometry for finding the addresses of the image matrix that belong to the cell to coloured.
*Example Call: colourCell(img, 3, 5, 1, 200)
'''
##  colourCell function takes 5 arguments:-
##            img - input image
##            level - level of cell to be coloured
##            cellnum - cell number of cell to be coloured
##            size - size of maze
##            colourVal - the intensity of the colour.
##  colourCell basically highlights the given cell by painting it with the given colourVal. Care should be taken that
##  the function doesn't paint over the black walls and only paints the empty spaces. This function returns the image
##  with the painted cell.
def colourCell(img, level, cellnum, size, colourVal):
    ############################# Add your Code Here ################################
    if size == 1:
        s = 220
    else:
        s = 300
    if level == 1:
        t = 60
    elif level == 2:
        t = 30
    elif level == 3 or level == 4 or level == 5:
        t = 15
    elif level == 6:
        t = 7.5
    if (level == 0 ):
        for i in range(0,41):
            for j in range(0,360):
                if(img[s + i*sine(j),s + i*cosine(j)] > 127):               #trying to colour only bright areas
                    img[s + i*sine(j),s + i*cosine(j)]=colourVal
    else:
        b = np.arange((cellnum-1)*t,cellnum*t+1,0.15)                       # making the angles lesser intervals like 0.15, lesser the intervals more the execution time,smoother the image
        for i in range(level*40,(level+1)*40+1):
            for j in b:
                if(img[s + i*sine(j),s + i*cosine(j)] > 127):
                    img[s + i*sine(j),s + i*cosine(j)]=colourVal
    #################################################################################
    return img

'''
*Function Name: buildGraph
*Input: img->image matrix, size-> size flag of the image.
*Output: The graph of the maze image.
*Logic: Building graph using the findNeghbours(...) function for finding neighbours of each cell.
*Example Call: buildGraph(img, 2)
'''
##  Function that accepts some arguments from user and returns the graph of the maze image.
def buildGraph(img):   ## You can pass your own arguments in this space.
    graph = {}
    ############################# Add your Code Here ################################
    for i in range(0,5):
        if(i==0):
            graph[(0,0)] = findNeighbours(img,0,0)                             #finding the neighbours and adding them to the graph.
        if(i==1):
            for j in range(1,5):
                graph[(i,j)] = findNeighbours(img,i,j)
        if(i==2):
            for j in range(1,11):
                graph[(i,j)] = findNeighbours(img,i,j)
        if(i==3):
            for j in range(1,16):
                graph[(i,j)] = findNeighbours(img,i,j)
        if(i==4):                                                     #level will be equal to 5 or 6, only when the size is 2 i.e. 600x600.
            for j in range(1,21):
                graph[(i,j)] = findNeighbours(img,i,j)

    #################################################################################
    return graph

'''
*Function Name: findStartPoint
*Input: img->image matrix, size-> size flag of the image.
*Output: The Start coordinates of the maze.
*Logic: finding the missing wall in the outermost cell.
*Example Call: findStartPoint(img,2)
'''
##  Function accepts some arguments and returns the Start coordinates of the maze.
def findStartPoint(img,size):     ## You can pass your own arguments in this space.
    ############################# Add your Code Here ################################
    if(size == 1):
        for cellnum in range(1,25):
            if img[220 + 40*5*sine((360/24)*(cellnum-0.5)),220 + 40*5*cosine((360/24)*(cellnum-0.5))] > 127:            #checking the walls of fourth cell for smaller image.
                start = (4,cellnum)
    else:
        for cellnum in range(1,49):
            if img[300 + 40*7*sine(7.5*(cellnum-0.5)),300 + 40*7*cosine(7.5*(cellnum-0.5))] > 127:                      #checking the walls of sixth cell for bigger image.
                start = (6,cellnum)
                break

    #################################################################################
    return start

'''
*Function Name: findPath
*Input: graph->graph of the image, start->coordinates of the start point, end->coordinates of the end point, path->optional input for finding the shortest path using recursion.
*Output: Set of coordinates from initial point to final point.
*Logic: using simple shortest path fing algorithm for a graph.
*Example Call: findPath(graph,(0,0),(9,9))
'''
##  Finds shortest path between two coordinates in the maze. Returns a set of coordinates from initial point
##  to final point.
def findPath(graph,start,end,path=[]):      ## You can pass your own arguments in this space.
    ############################# Add your Code Here ################################
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = findPath(graph, node, end, path)               ##Using recursion to find the shortest path.
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath

    #################################################################################
    return shortest
def step(l):
    if l==4:
        m = 20
    elif l==3:
        m = 15
    elif l == 2:
        m = 10
    elif l==1:
        m = 4
    elif l == 0:
        m = 1
    return 360/m
def laser_angle(l):
    if l==4:
        la = 33
    elif l==3:
        la = 39
    elif l == 2:
        la = 49
    elif l==1:
        la = 65
    elif l==0:
        la = 85
    return la
def laser_angle2(l):
    if l==4:
        la = 146
    elif l==3:
        la = 139
    elif l == 2:
        la = 130
    elif l==1:
        la = 117
    elif l==0:
        la = 85
    return la


def send(msg):
    global message
    while(1):
        if message == "Executed":
            print msg
            message= ""
            mqttc.publish(MQTT_TOPIC,msg)
            break
def toBaseStation():
    filePath = "MAP.jpg"
    img = readImage(filePath)     ## Read image with specified filepath
    markers = findMarkers(img)
    print markers
    op = findOptimumPath(img,markers)
    if op[0][0]==(4,1) and op[0][1]==(4,20):
            del op[0][0]
    pl,pc = op[0][0]
    offset = 30
    aangle = offset
    global message
    send("a000")
    send("l000")
    send("l033")
    send("a030")
    flag = 1
    for path in op:
        for cd in path:
            print cd
            l,c = cd
            if pl > l:
                aangle = offset+(pc-1)*step(pl)+step(pl)/2
                if aangle>180 and paangle<180:
                    send("a180")
                    send("a000")
                    if flag != 2:
                            send("l"+str("%03d"%laser_angle2(pl)))
                            flag = 2
                    send("a"+str("%03d"%(aangle-180)))
                    send("l"+str("%03d"%laser_angle2(l)))
                elif aangle<180 and paangle>180:
                    send("a180")
                    send("a000")
                    if flag!=1:
                            send("l"+str("%03d"%laser_angle(pl)))
                            flag = 1
                    send("a"+str("%03d"%aangle))
                    send("l"+str("%03d"%laser_angle(l)))
                else:
                    if aangle>180:
                        send("a"+str("%03d"%(aangle-180)))
                    elif aangle<180:
                        send("a"+str("%03d"%aangle))
                    if flag == 1:
                        send("l"+str("%03d"%laser_angle(l)))
                    elif flag == 2:
                        send("l"+str("%03d"%laser_angle2(l)))
                    
            elif pl<l:
                aangle = offset+(c-1)*step(l)+step(l)/2
                if aangle>180 and paangle<180:
                    send("a180")
                    send("a000")
                    if flag != 2:
                            send("l"+str("%03d"%laser_angle2(pl)))
                            flag = 2
                    send("a"+str("%03d"%(aangle-180)))
                    send("l"+str("%03d"%laser_angle2(l)))
                elif aangle<180 and paangle>180:
                    send("a180")
                    send("a000")
                    if flag!=1:
                            send("l"+str("%03d"%laser_angle(pl)))
                            flag = 1
                    send("a"+str("%03d"%aangle))
                    send("l"+str("%03d"%laser_angle(l)))
                else:
                    if aangle>180:
                        send("a"+str("%03d"%(aangle-180)))
                    elif aangle<180:
                        send("a"+str("%03d"%aangle))
                    if flag == 1:
                        send("l"+str("%03d"%laser_angle(l)))
                    elif flag == 2:
                        send("l"+str("%03d"%laser_angle2(l)))
            pl = l
            pc = c
            paangle = aangle
        #print "a"+str(offset+(c-1)*step(l)+step(l)/2)
        aangle = offset+(c-1)*step(l)+step(l)/2
        if aangle>180 and paangle<180:
            send("a180")
            send("a000")
            if flag != 2:
                    send("l"+str("%03d"%laser_angle2(pl)))
                    flag = 2
            send("a"+str("%03d"%(aangle-180)))
            send("l"+str("%03d"%laser_angle2(l)))
        elif aangle<180 and paangle>180:
            send("a180")
            send("a000")
            if flag!=1:
                    send("l"+str("%03d"%laser_angle(pl)))
                    flag = 1
            send("a"+str("%03d"%aangle))
            send("l"+str("%03d"%laser_angle(l)))
        else:
            if aangle>180:
                send("a"+str("%03d"%(aangle-180)))
            elif aangle<180:
                send("a"+str("%03d"%aangle))
            if flag == 1:
                send("l"+str("%03d"%laser_angle(l)))
            elif flag == 2:
                send("l"+str("%03d"%laser_angle2(l)))
        paangle = aangle
        print "checkpoint"


def on_message(mosq, obj, msg):
    global message
    message = msg.payload
    print message
    
def mqtt_subscriber():
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe
    mqttc.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    mqttc.loop_forever()
##  This is the main function where all other functions are called. It accepts filepath
##  of an image as input. You are not allowed to change any code in this function. You are
##  You are only allowed to change the parameters of the buildGraph, findStartPoint and findPath functions
'''def main(filePath, flag = 0):
    
        
    op1 = str(op)
    print op1
    mqttc = mqtt.Client("", True, None, mqtt.MQTTv31)
    mqttc.on_publish = on_publish
    mqttc.on_connect = on_connect
    mqttc.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    mqttc.publish(MQTT_TOPIC,op1)
    mqttc.disconnect()
    #maze_graph = buildGraph(img)
    #print maze_graph## Build graph from maze image. Pass arguments as required
    #start = findStartPoint(img,size)  ## Returns the coordinates of the start of the maze
    #shortestPath = findPath(maze_graph,(4,1),(0,0))  ## Find shortest path. Pass arguments as required.
    #print shortestPath
    #string = str(shortestPath) + "\n"
    #for i in shortestPath:               ## Loop to paint the solution path.
    #    img = colourCell(img, i[0], i[1], size, 230)
    if __name__ == '__main__':     ## Return value for main() function.
        return img
    else:
        if flag == 0:
            return string
        else:
            return graph'''
## The main() function is called here. Specify the filepath of image in the space given.
if __name__ == "__main__":
    Thread(target = mqtt_subscriber).start()
    Thread(target = toBaseStation).start()
