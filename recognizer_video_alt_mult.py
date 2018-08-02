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
import queue
import multiprocessing
from multiprocessing import Pool
import facePackages.FRP as FRP
import os, os.path, pickle, math
from sklearn import neighbors
from PIL import Image, ImageDraw
import numpy as np
import dlib
import cv2
import sys
from sys import stdout
import gc


video = input("----------- Enter the path to the video(including the .mp4): ")
start_time = time.time()
convert_video = cv2.VideoCapture(video)
length = int(convert_video.get(cv2.CAP_PROP_FRAME_COUNT))
fps = float(convert_video.get(cv2.CAP_PROP_FPS))
filename = input("----------- Enter the name of the resulting video (including the .avi): ")

classifier = input("----------- Please enter the path to the classifier you wish to use: ")

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
    
    
print("\rall frames read")   
print("step one complete") 


# Grab the file with the images to be recognised from the user
image_path = "preproc_frames"

# Get the classifier from the user


# for each image in the file recognise the faces in the image
files = []
for img in os.listdir(image_path):
	file_path = os.path.join(image_path, img)
	files.append(file_path)



def detectFaces(file_path):
	#print("----------- Look'n for a face in: {}".format(file_path))
	# pass the image to be recognized
	predict = FRP.recog(file_path, model_path=classifier)
	if len(predict) > 0:
		acc = predict[1]
		predict = predict[0]
	else:
		acc = []

		
	# for every name predicted output it to the console
	#for name, (top, right, bottom, left) in predict:
		#print("----------- Found {} at ({}, {})".format(name, left, top))
		# Show all the face with the names attached
	FRP.show_known_face_name(file_path, predict, acc)
			
	gc.collect()
	return 1
def mp_worker(files):
	if(multiprocessing.cpu_count() > 2):
		p = multiprocessing.Pool(4)
	else:
		p = multiprocessing.Pool(1)
	for i, _ in enumerate(p.imap(detectFaces, files), 1):
		sys.stderr.write('\rdone {0:%}'.format(i/length))
	p.close()
	p.join()
	return
if __name__ == '__main__':	
	mp_worker(files)

	



print("\rstep two complete") 

foldername = "preproc_frames"



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
print("\r--- %s seconds ---" % (time.time() - start_time))
print("step three complete!")