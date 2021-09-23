# Holo2 Python code to process holographic images and videos

PROGRAMS
========

**findZ.py** loads images from a directory and uses keyboard to adjust reconstruction Z and save reco image with Z value embedded in file name

**findZ_histogram** findZ.py program with a histogram plot of pixel intensity for reconstructed image

**findZ_line** findZ.py program with a plot of pixel intensity of the reconstructed image across the middle row 

**holoVideoReco.py** loads an mp4 videos, user selects frame, crops image, adjusts reconstruction Z, and saves raw and reco images

**detect.py** reads a video frame-by-frame, detects objects and saves location, area, and aspect ratio to a file

**arrayColorDemonstration.py** examples of how represent and manipulate images as numpy arrays and explore HSV color space

**examineReco.py** demonstrates how reconstruction works

**phaseAbbScan.py** visualizes the phase abberition calculations over a range of z values, to demonstrate how reconstruction works

**bouncingSquare.py** demonstrates creating and manipulating image numpy arrays using a bouncing red square as an example

**pyGame_PlayNoteInstrument.py** demonstrates playing notes on different midi instruments in the computer using pygame

**testTrack.py** functions useful for tracking objects



FUNCTIONS
==========

**keyboard.py** changes variables with keyboard while program is running

**reco.py** performs holographic reconstruction

================

Thomas Zimmerman, IBM Research-Almaden

Holgraphic Reconstruction Algorithms by Nick Antipac, UC Berkeley and  Daniel Elnatan, UCSF

This work is funded by the National Science Foundation (NSF) grant No. DBI-1548297, Center for Cellular Construction.
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation. 

