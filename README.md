# Code to process holographic images and videos

PROGRAMS
========

**Detect_MedianThresh.py** setect objects in video and save the dimensions of bounding boxes using background subtraction

**findZ.py** loads images from a directory and uses keyboard to adjust reconstruction Z and save reco image with Z value embedded in file name

**findZ_histogram** findZ.py program with a histogram plot of pixel intensity for reconstructed image

**findZ_line** findZ.py program with a plot of pixel intensity of the reconstructed image across the middle row 

**holoVideoReco.py** loads an mp4 videos, user selects frame, crops image, adjusts reconstruction Z, and saves raw and reco images

**focusGabor.py** autofocus program that run a stack of images through a 0 and 90 deg Gabor Filter and select the image with the highest Gabor value (indicating best focus)

**detect.py** reads a video frame-by-frame, detects objects and saves location, area, and aspect ratio to a file

**HSV_colorSpace.py** examples of how represent and manipulate images as numpy arrays and explore HSV color space

**examineReco.py** demonstrates how reconstruction works

**phaseAbbScan.py** visualizes the phase abberition calculations over a range of z values, to demonstrate how reconstruction works

**bouncingSquare.py** demonstrates creating and manipulating image numpy arrays using a bouncing red square as an example

**playNote.py** demonstrates playing notes on different midi instruments in the computer using pygame

**testTrack.py** functions useful for tracking objects

**streamRecoLine.py** interactive holographic reconstruction with Tkinter interface with line contrast display

**testStreamingVideo.py** find out the address of the microscope (as external USB camera) 

**HW6Task3_helper.py** assigns the IDs of the closest objects in the previous frame to the objects in the current frame (used for tracking)

**detectBlur.py** detect program with blur to try and prevent an object from having multiple bounding boxes

**playChords.py** play notes as a chord, arpeggiated, etc. Requires pyGame midi player.note

**renameFiles.py** renames files in a directory with an ascending number

**USB_CAM.docx** how to convert Raspberry Pi into a USB camera

FUNCTIONS
==========

**keyboard.py** changes variables with keyboard while program is running

**reco.py** performs holographic reconstruction

ACKNOWLEDGMENT 
==============

Code written by Thomas G. Zimmerman, IBM Research-Almaden and Center for Cellular Construction, except Holgraphic Reconstruction Algorithms by Nick Antipac, UC Berkeley and  Daniel Elnatan, UCSF.
This work is funded by the National Science Foundation (NSF) grant No. DBI-1548297, Center for Cellular Construction.
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation. 

