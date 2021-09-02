'''
Enables program variables to be adjusted with keyboard while program is running

Must define variables, starting values, key associated with variable, and return all variables

v1 09.02.2021
Tom Zimmerman CCC, IBM Research March 2020
This work is funded by the National Science Foundation (NSF) grant No. DBI-1548297, Center for Cellular Construction.
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation.
'''

import numpy as np
import cv2

keypad=['t','b','x','y']    # define what key character is associated with variable
keyValue=[76,2,4,6]         # define starting value
stepValue=[1,2,1,1]         # define scaling of value, i.e., how much variable changes with each key increment.... not implimented yet in V1
keyState=0;                 # the current selected key
keyBuf=np.zeros((256),dtype=int)    # where are the key values are stored (before scaling)
run=1                       # set to 0 if 'q' is hit, to end program

# initialize key buffer with starting values
for i in range(len(keypad)):
    keyBuf[ord(keypad[i])]=keyValue[i]

def processKey():
    global keyState,run;

    key=cv2.waitKey(500) # value is delay in milliseconds to slow down video, must be > 0
    if key!=-1:
        keyList=[ord('='),ord('-'),ord('+'),ord('_')]
        value=[1,-1,+10,-10]
        inc=0
        if key in keyList:
            index=keyList.index(key)
            inc=value[keyList.index(key)]
            keyBuf[keyState]+=inc
            if keyBuf[keyState]<0:
                keyBuf[keyState]=0
        else:
            keyState=key
        print (chr(keyState),'=',keyBuf[keyState])

        # update variables
        for i in range(len(keypad)):
            keyValue[i]=keyBuf[ord(keypad[i])]

        # check to see if user wants to quit program by pressing 'q' key
        if key==(ord('q')):
            run=0           # variable program checks to see if user wants to quit program
    return(keyValue)        # return all the variable values, must be received in the proper order!

