'''
Convert all video files in directory to mp4 format. Directory must only contain video files.
You will have to change the directory location (line 10) and where the ffmpeg.exe is located (line 23)
12.18.19 Thomas Zimmerman, IBM Research-Almaden
''

from os import listdir
from os.path import isfile, join
import subprocess

myPath=r'C:\Users\ThomasZimmerman\Videos\microscope\h264_Videos\\'   #directory must contain only video files

files = [f for f in listdir(myPath) if isfile(join(myPath, f))]

for f in files:
    print ('*'*20)
    if '.mp4' not in f:
        inFile=myPath+f
        a=f.split('.')
        outName=a[0]+'.mp4'
        outFile=myPath+outName
        print ('convert:',f, 'to',outName)
        subprocess.call([r'C:\Users\ThomasZimmerman\Videos\ffmpeg\\ffmpeg.exe','-i', inFile, '-c','copy', outFile])  # this is where the ffmpeg.exe is located
        print ('done')
        print
    else:
        print (f, 'already an mp4 file, skipped.')
    


