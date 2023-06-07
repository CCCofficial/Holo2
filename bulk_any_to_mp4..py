from os import listdir
from os.path import isfile, join
import subprocess

#myPath=r'C:\Users\ThomasZimmerman\Videos\SFSU_test\\'
#myPath=r'C:\Users\ThomasZimmerman\Videos\Aquaponic\Brian\\'
#myPath=r'C:\Users\ThomasZimmerman\Videos\microscope\Sujoy Annotated\\'
#myPath=r'C:\Users\ThomasZimmerman\Videos\microscope\Hologram\fewPlankton\\'
myPath=r'C:\Users\ThomasZimmerman\Videos\microscope\Village Microscope\videoC\\'

files = [f for f in listdir(myPath) if isfile(join(myPath, f))]

for f in files:
    print ('*'*20)
    if '.mp4' not in f:
        inFile=myPath+f
        a=f.split('.')
        outName=a[0]+'.mp4'
        outFile=myPath+outName
        print ('convert:',f, 'to',outName)
        subprocess.call([r'C:\Users\ThomasZimmerman\Videos\ffmpeg\\ffmpeg.exe','-i', inFile, '-c','copy', outFile])
        print ('done')
        print
    else:
        print (f, 'already an mp4 file, skipped.')
    


