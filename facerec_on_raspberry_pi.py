# This is a demo of running face recognition on a Raspberry Pi.
# This program will print out the names of anyone it recognizes to the console.

# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

import picamera
import numpy as np
import facePackages.FRP as FRP
import os, os.path, pickle, math
from sklearn import neighbors
from PIL import Image, ImageDraw
import dlib
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

print("----------- Welcome to the face recognition program!")

# Get the classifier from the user
classifier = input("----------- Please enter the path to the classifier you wish to use: ")

# Load a sample picture and learn how to recognize it.



# Initialize some variables

while True:
    print("Capturing image.")
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")
    # Find all the faces and face encodings in the current frame of video


    predict = FRP.recog_from_vid(output, model_path=classifier)
    # Loop over each face found in the frame to see if it's someone we know.
	
    for name, (top, right, bottom, left) in predict:
        print("----------- Found {} at ({}, {})".format(name, left, top))

