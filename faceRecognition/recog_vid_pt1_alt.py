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




video = input("----------- Enter the path to the video(including the .mp4): ")
convert_video = cv2.VideoCapture(video)
length = int(convert_video.get(cv2.CAP_PROP_FRAME_COUNT))


i = 0
while True:
    
    # loop through the video and increment the frame number
    ret, frame = convert_video.read()
    
    # if out of frames then break the while loop
    if not ret:
        break
    image = Image.fromarray(frame)
    mode = 'RGB'
    the_image = image.convert(mode)
    draw = ImageDraw.Draw(the_image)
    stri = str(i)
    j = 0
    if length - i < 10:
        j = 5
    elif length - i < 100:
        j = 4
    elif length - i < 1000:
        j = 3
    elif length - i < 10000:
        j = 2
    elif length - i < 100000:
        j = 1
    elif length - i < 1000000:
        j = 0
    width = j

        
    stri = stri.rjust(width, '0')
    file_path = os.path.join("preproc_frames", stri)
    
    
     # create the known faces directory if not already created
    if not (os.path.exists("preproc_frames")):
        os.makedirs("preproc_frames")
     
     # saves the image with a new name in the known faces directory
    the_image.save('preproc_frames/{}.jpg'.format(os.path.split(file_path)[1]))
    i = i + 1
    

print("all frames read")   
print("step one complete, run recognizer_mult.py on resulting images for step 2") 