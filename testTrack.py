'''
Functions useful for tracking objects

v1 09.23.2021
Tom Zimmerman CCC, IBM Research March 2020
This work is funded by the National Science Foundation (NSF) grant No. DBI-1548297, Center for Cellular Construction.
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation.
'''

import numpy as np

detectFileName='detection.csv'      # output file containing object location, area, aspect ratio for each video frame
FRAME=0; ID=1;  X0=2;   Y0=3;   X1=4;   Y1=5;   XC=6;   YC=7; AREA=8; AR=9; ANGLE=10; MAX_COL=11 # pointers to detection features

data=np.loadtxt(detectFileName,delimiter=',',skiprows=1)
print('data shape',data.shape)

maxFrames=len(np.unique(data[:,FRAME]))
print('max frames',maxFrames)

# get index of all rows with Frame==1
frame1_index=np.where(data[:,FRAME]==1)
print('frame1_index',frame1_index,'type',type(frame1_index))

# a tuple is an immutable list (values can't be changed)
f1=frame1_index[0]
print('f1',f1,'shape',f1.shape)

# get index of all rows with Frame==2
f2=np.where(data[:,FRAME]==2)[0]
print('f2',f2,'shape',f2.shape)

# create list of object locations in frame 2
xc2=data[f2,XC]
print('xc2',xc2)
