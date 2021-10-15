# Draw bounding box around binary objects in each frame of video
# Uses blur to try and prevent one object from having multiple bounding boxes
# Press 'q' to quit

# V2 use full image
# 10/15/2021 Tom Zimmerman CCC, IBM Research  
# This work is funded by the National Science Foundation (NSF) grant No. DBI-1548297, Center for Cellular Construction.
# Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation.

############################## FOR EDUCATIONAL USE ONLY ####################
import numpy as np
import cv2

########## USER SETTINGS ##############################
vid=r'fiveSecondPlankton.mp4'    
detectFileName='test.csv'
X_REZ=640; Y_REZ=480; # viewing resolution
MIN_AREA=400    # min area of object detected
THICK=2         # bounding box line thickness
THRESH=85       # detection threshold
BLUR=7          # must be odd number, larger means more blur

############# DETECT OUTPUT ##################
detectHeader= 'FRAME,ID,X0,Y0,X1,Y1,XC,YC,AREA,AR,ANGLE'
FRAME=0; ID=1;  X0=2;   Y0=3;   X1=4;   Y1=5;   XC=6;   YC=7; AREA=8; AR=9; ANGLE=10; MAX_COL=11
detectArray=np.empty((0,MAX_COL), dtype='int') # cast as int since most features are int and it simplifies usage

def getAR(obj):
    ((xc,yc),(w,h),(angle)) = cv2.minAreaRect(obj)  # get parameters from min area rectangle
    ar=0.0      # initialize aspect ratio as a floating point so calculations are done in floating point
    # calculate aspect ratio (always 1 or greater)
    if w>=h and h>0:
        ar=w/h
    elif w>0:
        ar=h/w
    return(xc,yc,ar,angle)         

######### start capturing frames of video #############
# PROGRAMS START

cap = cv2.VideoCapture(vid)
frameCount=0
while(cap.isOpened()):
    
    # read key, test for 'q' quit
    key=cv2.waitKey(1) & 0xFF # pause 1 second (1000 msec)
    if key== ord('q'):
        break
    
    # get image
    ret, colorIM = cap.read()
    if not ret: # check to make sure there was a frame to read
        print('Can not find video or we are all done')
        break
    frameCount+=1
    
    # blur and threshold image
    grayIM = cv2.cvtColor(colorIM, cv2.COLOR_BGR2GRAY)    # convert color to grayscale image
    blurIM=cv2.medianBlur(grayIM,BLUR)                  # blur image to fill in holes to make solid object
    ret,threshIM = cv2.threshold(blurIM,THRESH,255,cv2.THRESH_BINARY_INV) # threshold image to make pixels 0 or 255

    # get contours  
    dummy,contourList, hierarchy = cv2.findContours(threshIM, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # all countour points, uses more memory
    
    # draw bounding boxes around objects
    objCount=0      # used as object ID in detectArray
    for objContour in contourList:                  # process all objects in the contourList
        area = int(cv2.contourArea(objContour))     # find obj area        
        if area>MIN_AREA:                           # only detect large objects       
            PO = cv2.boundingRect(objContour)
            x0=PO[0]; y0=PO[1]; x1=x0+PO[2]; y1=y0+PO[3]
            cv2.rectangle(colorIM, (x0,y0), (x1,y1), (0,255,0), THICK) # place GREEN rectangle around each object, BGR
            (xc,yc,ar,angle)=getAR(objContour)

            # save object parameters in detectArray in format FRAME=0; ID=1;  X0=2;   Y0=3;   X1=4;   Y1=5;   XC=6;   YC=7; CLASS=8; AREA=9; AR=10; ANGLE=11; MAX_COL=12
            parm=np.array([[frameCount,objCount,x0,y0,x1,y1,xc,yc,area,ar,angle]],dtype='int') # create parameter vector (1 x MAX_COL) 
            detectArray=np.append(detectArray,parm,axis=0)  # add parameter vector to bottom of detectArray, axis=0 means add row
            objCount+=1                                     # indicate processed an object
    print('frame:',frameCount,'objects:',len(contourList),'big objects:',objCount)

    # shows results
    VGA=(640,480)
    cv2.imshow('colorIM', cv2.resize(colorIM,VGA))      # display image
    cv2.imshow('threshIM', cv2.resize(threshIM,VGA))# display thresh image
    #if frameCount>100:
     #   break

if frameCount>0:
    print('Done with video. Saving feature file and exiting program')
    np.savetxt(detectFileName,detectArray,header=detectHeader,delimiter=',', fmt='%d')
    cap.release()
else:
    print('Count not open video',vid)
cv2.destroyAllWindows()








