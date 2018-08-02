#################################################################################
# 
#   - This program actually takes an image folder and runs the recognition
#       classifier on them then displays the image with the names overlayed
#
#   - You'll be prompted to provide paths to the images folder and classifier
#
#   - Image folder doesn't require any stucture to be passed in
#
#################################################################################


import time
import facePackages.FRP as FRP
import os, os.path, pickle, math
from sklearn import neighbors
from PIL import Image, ImageDraw
import numpy as np
import dlib
import cv2
import dlib
import sys
from sys import stdout

print("----------- Welcome to the face recognition program!")

video = input("----------- Enter the path to the video(including the .mp4): ")
convert_video = cv2.VideoCapture(video)
length = int(convert_video.get(cv2.CAP_PROP_FRAME_COUNT))

fps = float(convert_video.get(cv2.CAP_PROP_FPS))

filename = input("----------- Enter the name of the resulting video (including the .avi): ")

# create resulting video and set the frame rate and resolution of the video you're passing in
cc = cv2.VideoWriter_fourcc(*'VP80')
resulting_video = cv2.VideoWriter(filename, cc, fps, (int(convert_video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(convert_video.get(cv2.CAP_PROP_FRAME_HEIGHT))))

# Get the classifier from the user
classifier = input("----------- Please enter the path to the classifier you wish to use: ")
start_time = time.time()
# Load a sample picture and learn how to recognize it.


i = 0
# Initialize some variables

while True:
	
	# loop through the video and incrament the frame number
	ret, frame = convert_video.read()
	
	i += 1
	stdout.write("\r" + "writing frame {}".format(i) + " of {}".format(length))
	stdout.flush()
    # if out of frames then break the while loop
	if not ret:
		break
    
    # since the cv2 converts the img to BGR we need to convert it back to RGB
	#converted_rgb_frame = frame[:, :, ::-1]
	frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
	
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	predict = FRP.recog_from_vid(frame, model_path=classifier)
	
	
	if len(predict) > 0:
		acc = predict[1]
		predict = predict[0]
	else:
		acc = []
	# Loop over each face found in the frame to see if it's someone we know.
	image = FRP.show_known_face_name_from_vid(frame, predict, acc)
	open_cv_image = np.array(image)
	image = open_cv_image[:, :, ::-1].copy() 
	# show the frame
	resulting_video.write(image)

# cleanup
convert_video.release()
resulting_video.release()
cv2.destroyAllWindows()
print("--- %s seconds ---" % (time.time() - start_time))
