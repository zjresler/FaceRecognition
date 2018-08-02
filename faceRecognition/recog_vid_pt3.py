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

video = input("----------- Enter the path to the original video(including the .mp4) (used for grabbing metadata): ")
convert_video = cv2.VideoCapture(video)
length = int(convert_video.get(cv2.CAP_PROP_FRAME_COUNT))

fps = float(convert_video.get(cv2.CAP_PROP_FPS))

foldername = input("----------- Enter the name of the folder containing the files that are already processed: ")

filename = input("----------- Enter the name of the resulting video (including the .avi): ")
start_time = time.time()

# create resulting video and set the frame rate and resolution of the video you're passing in
cc = cv2.VideoWriter_fourcc(*'VP80')
resulting_video = cv2.VideoWriter(filename, cc, fps, (int(convert_video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(convert_video.get(cv2.CAP_PROP_FRAME_HEIGHT))))

i = 0

for img in sorted(os.listdir(foldername)):
    
    i += 1
    stdout.write("\r" + "writing frame {}".format(i) + " of {}".format(length))
    stdout.flush()
    file_path = os.path.join(foldername, img)

    the_image = Image.open(file_path).convert("RGB")
    
    open_cv_image = np.array(the_image)
    image = open_cv_image[:, :, ::-1].copy() 
    resulting_video.write(image)
    
dlib.hit_enter_to_continue
print("--- %s seconds ---" % (time.time() - start_time))
print("complete!")