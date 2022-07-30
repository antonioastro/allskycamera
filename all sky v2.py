#Thanks to R Sparrius for meteor detection code. See original post at: https://www.meteornews.net/2020/05/05/d64-nl-meteor-detecting-project/
#This code *should* take a capture of the sky using a Raspberry Pi camera, and automatically detect meteors in the image immediately. 
#If it does not detect any meteors it will delete the capture and repeat
#It could detect planes or satellites, which are also cool - you must check for these yourself but if they are detected then you can confirm the code is working

import numpy as np
import cv2 as cv
from picamera import PiCamera
from time import sleep
from datetime import datetime
import os
import time

#define necessary variables
start=21 #hour to start, rounded to start of hours (20=8pm)
end = 5 #hour to end, - these to be adjusted according to night hours
exp=10 #exposure per frame in seconds
i=1 #dummy variable
count=0 #count for number of meteors detected
t=int(time.strftime('%H')) #get current hour of time

#set up the camera
PiCamera().close() #ensure camera is initially closed
camera=PiCamera() #open up a camera instance
camera.resolution = (1280, 720) #lower resolution makes it more sensitive to meteors
camera.framerate=1/exp #camera framerate, calculated automatically
camera.shutter_speed = 1000000*exp #exposure time in microseconds. calculated automatically
#camera.exposure_mode = 'off'

try:
    while t>start-1 or t<end: #loop continues between selected start and end times
        print('frame', i) #shows how many frames have been taken - this line can be #hashed out
        now = datetime.now() #gets current date/time
        print(now)
        camera.capture('/home/antonio/Desktop/meteors/meteor%s.jpg' % now, use_video_port=True) #take picture
        image = cv.imread('/home/antonio/Desktop/meteors/meteor%s.jpg' % now) #open image up
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY) #convert to greyscale
        blur = cv.GaussianBlur(gray, (5,5), 0) #apply gaussian blur to remove noise
        canny = cv.Canny(blur, 100, 200, 3) #edge detector
        cv.imwrite('/home/antonio/Desktop/temp/image%s.jpg' % now,canny) #save file temporarily
        meteors = cv.HoughLinesP(canny, 1, np.pi/180, 25, minLineLength=50, maxLineGap=5) #check for meteors
        if meteors is None:
            mainfile=str('/home/antonio/Desktop/meteors/meteor%s.jpg' % now)
            #os.remove(mainfile)#delete original image if no meteors
            tempfile=str('/home/antonio/Desktop/temp/image%s.jpg' % now)
            #os.remove(tempfile)#delete the temp file if no meteors
        else: #else move on, keep both main and temp frames
            count+=1
        i+=1
        print('Detected', count, 'meteors so far') #just an on going reminder of how many meteors caught, line can be hashed out
    camera.close()
except KeyboardInterrupt:
    camera.close()
print('end')