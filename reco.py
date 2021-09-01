'''
Supporting functions for Holographic Reconstruction with Tkinter interface
Thomas Zimmerman, IBM Research-Almaden 

Holgraphic Reconstruction Algorithms by Nick Antipac, UC Berkeley and  Daniel Elnatan, UCSF
This work is funded by the National Science Foundation (NSF) grant No. DBI-1548297, Center for Cellular Construction.
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation. 

V4 09.01.21 Force image to have even dimensions, clip ampIM to 0,255 to prevent rollover during 8 bit conversion
V3 03.01.21 removed unused background subtraction code
V2 03.01.21 added description of program
V1 09.24.19
'''
import cv2
import numpy as np

def openVid(vid):
    cap = cv2.VideoCapture(vid)
    return(cap)

def getFrame(cap,index):
    cap.set(cv2.CAP_PROP_POS_FRAMES,index)        # point to requested frame
    ret, rawFrame = cap.read()
    print('get frame status',cap,ret)
    return(ret,rawFrame)

def propagate(input_img, wvlen, zdist, dxy):
    M, N = input_img.shape # get image size, rows M, columns N, they must be even numbers!
    
    # prepare grid in frequency space with origin at 0,0
    _x1 = np.arange(0,N/2)
    _x2 = np.arange(N/2,0,-1)
    _y1 = np.arange(0,M/2)
    _y2 = np.arange(M/2,0,-1)
    _x  = np.concatenate([_x1, _x2])
    _y  = np.concatenate([_y1, _y2])
    x, y  = np.meshgrid(_x, _y)
    kx,ky = x / (dxy * N), y / (dxy * M)
    kxy2  = (kx * kx) + (ky * ky)

    # compute FT at z=0
    E0 = np.fft.fft2(np.fft.fftshift(input_img))

    # compute phase aberration 
    _ph_abbr   = np.exp(-1j * np.pi * wvlen * zdist * kxy2)
    output_img = np.fft.ifftshift(np.fft.ifft2(E0 * _ph_abbr))
    return output_img

def recoFrame(cropIM,z): 
    # holo microscope settings
    dxy   = 1.4e-6      # imager pixel (meters)
    wvlen = 650.0e-9    # wavelength of light is red, 650 nm

    #make even coordinates
    (yRez,xRez)=cropIM.shape
    if (xRez%2)==1:
        xRez-=1
    if (yRez%2)==1:
        yRez-=1
    cropIM=cropIM[0:yRez,0:xRez]

    res = propagate(np.sqrt(cropIM), wvlen, z, dxy)	 # calculate wavefront at z
    amp=np.abs(res)**2              # output is the complex field, compute intensity
    amp = np.clip(amp,0,255)        # prevent rollover when converting to 8 bit
    ampInt=amp.astype('uint8')  
    return(ampInt)


