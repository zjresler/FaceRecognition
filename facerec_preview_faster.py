import queue
import threading
from threading import Thread
import numpy as np
import facePackages.FRP as FRP
import os, os.path, pickle, math
from sklearn import neighbors
from PIL import Image, ImageDraw
import dlib
import time
from cv2 import *
import io



def do_stuff(q):

	frame = q.get()
	frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
	image = frame
	predict = FRP.recog_from_vid(image, model_path=classifier)
	# Loop over each face found in the frame to see if it's someone we know.
	image = FRP.show_known_face_name_from_vid(image, predict)
	open_cv_image = np.array(image)
	image = open_cv_image[:, :, ::-1].copy() 
	# show the frame
	rq.put(image)


	q.task_done()


q = queue.Queue(maxsize=0)
rq = queue.Queue(maxsize=0)
num_threads = 3
t = 0

	
cap = cv2.VideoCapture(0)



print("----------- Welcome to the face recognition program!")

# Get the classifier from the user
#classifier = input("----------- Please enter the path to the classifier you wish to use: ")
classifier = "zack.clf"
image = None
# Load a sample picture and learn how to recognize it.
while (True):
	while(q.qsize() < 3):
		ret, frame = cap.read()
		print(type(frame))
		q.put(frame)
		time.sleep(1/30)

	while t < num_threads:
		worker = Thread(target=do_stuff, args=(q,))
		worker.setDaemon(True)
		worker.start()
		t += 1

	t -= 1
	
	while(rq.qsize() > 0):
		image = rq.get()
		cv2.imshow("Frame", image)
		time.sleep(1/30)
	

	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	
	# clear the stream in preparation for the next frame
	key = cv2.waitKey(1) & 0xFF
	# if the `q` key was pressed, break from the loop
	#print(t)
	if key == ord("q"):
		break
		rq.task_done()
worker.join()
rq.join()
q.join()