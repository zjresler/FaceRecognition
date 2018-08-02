#################################################################################
# 
#   - This program actually takes an image folder and runs the recognition
#	   classifier on them then displays the image with the names overlayed
#
#   - You'll be prompted to provide paths to the images folder and classifier
#
#   - Image folder doesn't require any stucture to be passed in
#
#################################################################################


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


print("----------- Welcome to the face recognition program!")

# Grab the file with the images to be recognised from the user
image_path = input("----------- Please enter the path to the image you want to use: ")

# Get the classifier from the user
classifier = input("----------- Please enter the path to the classifier you wish to use: ")

# for each image in the file recognise the faces in the image
start_time = time.time()
files = []
for img in os.listdir(image_path):
	file_path = os.path.join(image_path, img)
	files.append(file_path)



def detectFaces(file_path):
	print("----------- Look'n for a face in: {}".format(file_path))
	# pass the image to be recognized
	predict = FRP.recog(file_path, model_path=classifier)
	if len(predict) > 0:
		acc = predict[1]
		predict = predict[0]
	else:
		acc = []

		
	# for every name predicted output it to the console
	for name, (top, right, bottom, left) in predict:
		print("----------- Found {} at ({}, {})".format(name, left, top))
		# Show all the face with the names attached
	FRP.show_known_face_name(file_path, predict, acc)
			
	gc.collect()
	return
	
def mp_worker(files):
	if(multiprocessing.cpu_count() > 2):
		p = multiprocessing.Pool(3)
		p.map(detectFaces, files)
	else:
		p = multiprocessing.Pool(1)
		p.map(detectFaces, files)
		
	p.close()
	p.join()
	return
if __name__ == '__main__':	
	mp_worker(files)
	print("--- %s seconds ---" % (time.time() - start_time))	
	dlib.hit_enter_to_continue()

cv2.destroyAllWindows()	

