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

i=1 #temp variable
count=0 #count number of meteors detected

camera=PiCamera() #redefine PiCamera to be easier to use
camera.resolution = (1280, 720)
camera.framerate=0.5
camera.shutter_speed = 2000000 #shutter speed in milliseconds
#camera.exposure_mode = 'off'

while i>0: #loop never stops until force stop
    print('exposure', i) #shows how many grabs have been taken
    now = datetime.now() #gets current date/time
    camera.capture('/home/antonio/Desktop/meteors/meteor%s.jpg' % now) #take picture
    image = cv.imread('/home/antonio/Desktop/meteors/meteor%s.jpg' % now) #open image up
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY) #convert to greyscale
    blur = cv.GaussianBlur(gray, (5,5), 0) #apply gaussian blur to remove noise
    canny = cv.Canny(blur, 100, 200, 3) #edge detector
    cv.imwrite('/home/antonio/Desktop/temp/image%s.jpg' % now,canny) #save file temporarily
    meteors = cv.HoughLinesP(canny, 1, np.pi/180, 25, minLineLength=50, maxLineGap=5) #check for meteors
    if meteors is None:
        mainfile=str('/home/antonio/Desktop/meteors/meteor%s.jpg' % now)
        os.remove(mainfile)#delete original image if no meteors
        tempfile=str('/home/antonio/Desktop/temp/image%s.jpg' % now)
        os.remove(tempfile)#delete the temp file if no meteors
    else: #else move on
        count+=1
        print('Detected', count, 'meteors so far')
    i+=1