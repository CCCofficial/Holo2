'''
Demonstrate creating and manipulating image numpy arrays using a bouncing red square as an example

Tom Zimmerman CCC, IBM Research September 16, 2020
This work is funded by the National Science Foundation (NSF) grant No. DBI-1548297, Center for Cellular Construction.
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation.
'''

import numpy as np
import cv2

XREZ=800
YREZ=500
COLOR_CHANNELS=3
DELAY=10     # delay in milliseconds, 0 means wait until keypress

print('start program')

# create array for image    
im=np.zeros((YREZ,XREZ,COLOR_CHANNELS),dtype='uint8')

# define red square
MAX_LOOP=1000
W=50;   H=50;
x0=0;   x1=x0+W;
y0=0;   y1=y0+H;
RED_CH=2                    # B,G,R
step=5
incX=step
incY=step
key=-1      # when key pressed this value is not -1

# render bouncing square in loop
while (key==-1):
    # move square
    x0+=incX
    y0+=incY
    x1=x0+W;
    y1=y0+H;

    # check for bounce off boundary
    if x1>XREZ:
        incX=-1*step
    elif x0<0:
        incX=step
    if y1>YREZ:
        incY=-1*step
    elif y0<0:
        incY=step

    # reset image and place square in image
    im[:,:,:]=0; # make all pixels black
    im[y0:y1,x0:x1,RED_CH]=255
    cv2.imshow('red square',im)
    key=cv2.waitKey(DELAY)
    
cv2.destroyAllWindows()     # close windows
print('bye!')


