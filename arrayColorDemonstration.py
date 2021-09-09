'''
Demonstrate Numpy array functions for images and color space

v2 9.9.21 
Tom Zimmerman CCC, IBM Research March 2020
This work is funded by the National Science Foundation (NSF) grant No. DBI-1548297, Center for Cellular Construction.
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation.
'''

import numpy as np
import cv2

imageTom=r'Tom.jpg'
imageBalloons=r'Balloons.jpg'
XREZ=400
YREZ=200
COLOR_CHANNELS=3
DELAY=0     # delay in milliseconds, 0 means wait until keypress

print('start program')

# create array for image    
im=np.zeros((YREZ,XREZ,COLOR_CHANNELS),dtype='uint8')
imCopy=im
imTrueCopy=np.copy(im)
print('im shape',im.shape)

# show blank image
cv2.imshow('blank image',im)
cv2.waitKey(DELAY)              # 0 means wait until window closed

# add a red square
x0=100; x1=200;
y0=50;  y1=100;
RED_CH=2                    # B,G,R
im[y0:y1,x0:x1,RED_CH]=255
cv2.imshow('red square',im)
cv2.waitKey(DELAY)  

# draw a green bounding rectangle using cv2
p1 = (x0,y0)        # represents the top left corner of rectangle
p2 = (x1,y1)        # represents the bottom right corner of rectangle
color = (0, 255, 0) # green (B,G,R)
thickness = 1        # line thickness in pixels
cv2.rectangle(im, p1, p2, color, thickness)
cv2.imshow('green rectangle',im)
cv2.waitKey(DELAY)  

# increase the line thickness
thickness = 20       # line thickness in pixels
cv2.rectangle(im, p1, p2, color, thickness)
cv2.imshow('thickness=20',im)
cv2.waitKey(DELAY)  

# what's the difference between imCopy=im and imTrueCopy=np.copy(im)?
cv2.imshow('imCopy',imCopy)
cv2.imshow('imTrueCopy',imTrueCopy)
cv2.waitKey(DELAY)  

# make blue rectangle solid
im=np.zeros((YREZ,XREZ,COLOR_CHANNELS),dtype='uint8') # recreate blank image
color = (255, 0, 0) # blue (B,G,R)
thickness =-1       # -1 thickness means fill in rectangle
cv2.rectangle(im, p1, p2, color, thickness)
cv2.imshow('blue solid',im)
cv2.waitKey(DELAY)  

# get image
colorIM = cv2.imread(imageTom)     #Read the image as grayscale
print('colorIM shape',colorIM.shape)
grayIM = cv2.imread(imageTom, 0) #Read the image as grayscale
print('load as gray',grayIM.shape)
gray2IM = cv2.cvtColor(colorIM, cv2.COLOR_BGR2GRAY)
print('convert to gray',gray2IM.shape)
cv2.imshow('colorIM',colorIM)
cv2.imshow('load as gray',grayIM)
cv2.imshow('convert to gray',gray2IM)
cv2.waitKey(DELAY)

# resize image, absolute size
dim=(200,100)
smallIM = cv2.resize(colorIM, dim)
cv2.imshow('imSmall',smallIM)
cv2.waitKey(DELAY)

# resize image, scaled size
scale_percent = 50          # percent of original size
(height,width,colorChannels)=colorIM.shape
height= int(height * scale_percent / 100)
width = int(width * scale_percent / 100)
dim = (width, height)               
imScale = cv2.resize(colorIM, dim)
cv2.imshow('imScale',imScale)
cv2.waitKey(DELAY)

# crop image
W=140; H=120;
x0=50; x1=x0+W;
y0=20;  y1=y0+H;
p1 = (x0,y0)                    # top left corner of rectangle
p2 = (x1,y1)                    # bottom right corner of rectangle
cropIM = colorIM[y0:y1,x0:x1,:] # crop image with all the color channels
cv2.imshow('cropIM',cropIM)
cv2.waitKey(DELAY)

# exploring color channels
colorIM = cv2.imread(imageBalloons)     # Read the image  
blueIM=colorIM[:,:,0]                   # b,g,r
greenIM=colorIM[:,:,1]
redIM=colorIM[:,:,2]
cv2.imshow('blue',blueIM)
cv2.imshow('green',greenIM)
cv2.imshow('red',redIM)
cv2.imshow('colorIM',colorIM)
cv2.waitKey(DELAY)

# exploring HSV color space representation of image
colorIM = cv2.imread(imageBalloons)     # Read the image  
hsvIM = cv2.cvtColor(colorIM, cv2.COLOR_BGR2HSV)  # convert bgr image to hsv
hIM=hsvIM[:,:,0]                        # h,s,v
sIM=hsvIM[:,:,1]
vIM=hsvIM[:,:,2]
cv2.imshow('H',hIM)
cv2.imshow('S',sIM)
cv2.imshow('V',vIM)
cv2.imshow('colorIM',colorIM)
cv2.waitKey(DELAY)

cv2.waitKey(0)              # stay here until window closed
cv2.destroyAllWindows()     # close windows
print('bye!')


