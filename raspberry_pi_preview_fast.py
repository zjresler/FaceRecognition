# This is a demo of running face recognition on a Raspberry Pi.
# This program will print out the names of anyone it recognizes to the console.

# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65
import queue
from threading import Thread
import picamera
import numpy as np
import facePackages.FRP as FRP
from sklearn import neighbors
from PIL import Image, ImageDraw
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import io
# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32




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
num_threads = 15
t = 0









print("----------- Welcome to the face recognition program!")

# Get the classifier from the user
#classifier = input("----------- Please enter the path to the classifier you wish to use: ")
classifier = "zack.clf"
my_stream = io.BytesIO()
# Load a sample picture and learn how to recognize it.
while (True):
	camera.start_preview()
	time.sleep(20)
	camera.capture(my_stream, 'jpeg')
	
	frame = my_stream.array
	q.put(frame)
	while t < num_threads:
		worker = Thread(target=do_stuff, args=(q,))
		worker.setDaemon(True)
		worker.start()
		t += 1

	t -= 1
	image = rq.get()
	cv2.imshow("Frame", image)

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
