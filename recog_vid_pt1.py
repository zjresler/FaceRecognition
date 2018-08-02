import time
import queue
import threading
import multiprocessing
from multiprocessing import Pool
import numpy as np
import cv2
import sys
import facePackages.FRP as FRP
import os, os.path, pickle, math
from sklearn import neighbors
from PIL import Image, ImageDraw
import dlib
import gc
from sys import stdout




video = input("----------- Enter the path to the video(including the .mp4): ")
start_time = time.time()
convert_video = cv2.VideoCapture(video)
length = int(convert_video.get(cv2.CAP_PROP_FRAME_COUNT))


i = 0
while True:
    
    # loop through the video and increment the frame number
    ret, frame = convert_video.read()
    
    # if out of frames then break the while loop
    if not ret:
        break
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame)
    stri = str(i)
    j = 0
    zeroes = ""
    while (length - i) - (10 ** j) > 0:
        j = j + 1
    width = j    
    stri = stri.rjust(width, '0')
    file_path = os.path.join("preproc_frames", stri)
    
    
     # create the known faces directory if not already created
    if not (os.path.exists("preproc_frames")):
        os.makedirs("preproc_frames")
     
     # saves the image with a new name in the known faces directory
    image.save('preproc_frames/{}.jpg'.format(os.path.split(file_path)[1]))
    i = i + 1
    stdout.write("\r" + "saving frame {}".format(i) + " of {}".format(length))
    stdout.flush()
    
    
print("--- %s seconds ---" % (time.time() - start_time))
print("all frames read")   
print("step one complete, run recognizer_mult.py on resulting images for step 2") 