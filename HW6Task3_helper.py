#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HW6Task3_helper

This code matches the object in a second frame to the closest object in the first frame and copies the ID of the closest object in the first frame to the ID of the object in the second frame.

For HW6 Task 3 you need to modify this code so it works over all the frames in the video and saves the modified data array at track.csv (hint, use np.savetxt() command)
I've also included a flag ASSIGNED you can use so you don't assign an ID to more than one object.

Thomas Zimmerman, IBM Research-Almaden
This work is funded by the National Science Foundation (NSF) grant No. DBI-1548297, Center for Cellular Construction.
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation. 
"""

import numpy as np
import math

detectFileName='detection.csv'      # output file containing object location, area, aspect ratio for each video frame
FRAME=0; ID=1;  X0=2;   Y0=3;   X1=4;   Y1=5;   XC=6;   YC=7; AREA=8; AR=9; ANGLE=10; MAX_COL=11 # pointers to detection features

################# FUNCTION ###################
def distance(x2,y2,x1,y1):
    """calculate the distance of the objects in current frame to 
    objects in past frame"""
    return(math.sqrt((int(x2)-int(x1))**2 + (int(y2)-int(y1))**2))

#################### MAIN ####################
data=np.loadtxt(detectFileName,delimiter=',',skiprows=1)
print('data shape',data.shape)

maxFrames=len(np.unique(data[:,FRAME]))
print('max frames',maxFrames)

# get index of all rows with the frame we are interested in
# np.where returns a tuple containing an array, so we get to the array by rquesting the first element of the tuple with [0]
# for a detailed explaination of why np.where returns a tuple, see https://stackoverflow.com/questions/50646102/what-is-the-purpose-of-numpy-where-returning-a-tuple
a=np.where(data[:,FRAME]==1)
f1=np.where(data[:,FRAME]==1)[0]
f2=np.where(data[:,FRAME]==2)[0]
print('objects in frame2=',len(f1),'objects in frame1=',len(f1),'\n')
      
# create an array to store all the distances and ID's for all combinations of objects in frame 2 and 1
ID1=0; D=1; ASSIGNED=2; # ID1 is ID of object in Frame 1, D is distance, ASSIGNED is a flag you can use to indicate the object in frame 1 has been assigned

#Make nested loop; outer loop is Frame 2 objects, inner loop is Frame 2 objects
for i2 in f2:       # process all objects in frame 2
    x2 = data[i2,XC] 
    y2 = data[i2,YC]
    index=0         # index to examine each object in frame 1
    comboArray=np.zeros((len(f1),3)) # create array to save distance calculations and ID's for each object in frame 1 
    for i1 in f1:   # process all objects in frame 1
        x1 = data[i1,XC]    
        y1 = data[i1,YC]
        d = distance(x2,y2,x1,y1)
        comboArray[index,ID1]=int(data[i1,ID])  # Save the ID and distances. ID is always an int, not a float.
        comboArray[index,D]=d
        print('Frame2 row=',i2,'Frame1 row=',i1,'distance=',round(d))  
        index+=1    # prepare for the object in frame 1

    # learn about np.argsort() see https://opensourceoptions.com/blog/sort-numpy-arrays-by-columns-or-rows/
    dSort=np.argsort(comboArray[:,D]) # sort comboArray by distance column (D). Returns an array of the rows, sorted by ascending value of the distance column!
    print('Best matching object has ID=',int(comboArray[dSort[0],ID1]),'at a distance=',round(comboArray[dSort[0],D]),'\n')

    # assign id of closest object in previous frame to object in current frame
    data[i2,ID]=comboArray[dSort[0],ID1] # write the ID of the closest object in frame 1 into the ID of object in frame 2
