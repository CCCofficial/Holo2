'''
Test streaming microscope
Press any key to end program

Tom Zimmerman CCC, IBM Research March 2020
This work is funded by the National Science Foundation (NSF) grant No. DBI-1548297, Center for Cellular Construction.
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation.
'''
import cv2

TEST_CAM=0          # set to 1 to scan all camera addresses
MICROSCOPE_CAM=0    # depends on your computer, use TEST_CAM=1 to discover

if TEST_CAM:
    MAX_CAM = 10
    for i in range(0, MAX_CAM):
        cap = cv2.VideoCapture(i)
        test, frame = cap.read()
        if test:
            print('camera',i,'result',str(test))
            cv2.imshow('cam='+str(i),frame)
            key=cv2.waitKey(30)
    key=cv2.waitKey(3000)
    
else:
    cap = cv2.VideoCapture(MICROSCOPE_CAM)  # select external web camera (microscope)
    cap.set(3, 1920); cap.set(4, 1080);     # set to 1080p resolution
    goodVideo, frame = cap.read()
    key=cv2.waitKey(30)

    while (goodVideo and key==-1) :
        goodVideo, frame = cap.read()
        cv2.imshow('Microscope',frame)
        key=cv2.waitKey(30)
    
cap.release()
cv2.destroyAllWindows()
