# GROCERY_APP (ver 2)
# USAGE
# python webstreaming.py --ip 0.0.0.0 --port 8000

""" Create a new function to read the video stream and extract the information
(frame + data of object). Let's do this!!  """

# import the necessary packages

from pyimagesearch.barcode_detection import BarcodeDetector
from imutils.video import VideoStream
from flask import Response
from flask import Flask, render_template, request, jsonify
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import threading
import argparse
import datetime
import imutils
import time
import cv2
import json

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None
lock = threading.Lock()

app = Flask(__name__)

# Retrieves the current datetime and displays it
def getTime():
	t = datetime.datetime.now()
	return t.strftime("%Y") + "-" + t.strftime("%m") + "-" + t.strftime("%d");

# sets one of the template pages for the App
@app.route('/add_new.html')
def addNew():
    return render_template('add_new.html', item_name=getData())

# listing page
@app.route("/listing.html")
def listing():
	return render_template("listing.html")

# javascript file
@app.route("/js/jquery-1.9.1.min.js")
def loadJS():
	return render_template("/js/jquery-1.9.1.min.js")

Base = declarative_base()
class Food(Base):
	__tablename__ = 't_food'
	id = Column(Integer, primary_key=True)
	item = Column(String)
	amount = Column(Integer)
	category = Column(String)
	expiry_date = Column(String)
	putin_date = Column(String)
	picture = Column(String)
	notes = Column(String)
	is_deleted = Column(Integer)
	def toJSON(self):
		my_list_keys = ["id", "item", "amount", "category", "expiry_date", "putin_date", "picture", "notes", "is_deleted"]
		my_list_values = [self.id, self.item, self.amount, self.category, str(self.expiry_date), str(self.putin_date), self.picture, self.notes, self.is_deleted]
		self.dictZip = zip(my_list_keys, my_list_values)
		return dict(self.dictZip)

	def __repr__(self):
		return '''{"item":'%s', "amount":'%s', "category":'%s', "expiry_date":'%s', "putin_date":'%s'}''' % (self.item, self.amount, self.category, self.expiry_date, self.putin_date)


#The method to show all the food data
@app.route("/getAllList.do", methods=['GET'])
def show():
	engine = create_engine("mysql://webapp:12345678@localhost:3306/fridge_screen", echo=True)
	Session = sessionmaker(bind=engine)
	session = Session()

	foodList = []
	for instance in session.query(Food):
		print(instance)
		jsonFood = instance.toJSON()
		foodList.append(jsonFood)
	return jsonify(foodList)


#The method to call to insert data to the database
@app.route("/add.do",methods=['POST'])
def insert():
	print(request.form)
	item = request.form["item"]
	amount = request.form["amount"]
	category = request.form["category"]
	expiry_date = request.form["expiry_date"]

	engine = create_engine("mysql://webapp:12345678@localhost:3306/fridge_screen", echo=True)
	Session = sessionmaker(bind=engine)
	session = Session()

	for instance in session.query(Food):
		print(instance)

	session = Session()
	test_food = Food(item=item, amount=amount, category=category, expiry_date=expiry_date, putin_date=getTime(), is_deleted=0)
	print(test_food)
	session.add(test_food)
	session.commit()
	print(test_food)
	return "hhh"


# initialize the video stream and allow the camera sensor to
# warmup
# use the webcam source
vs = VideoStream(src=0).start()
time.sleep(2.0)

item_name = "hhh"

def getData():
	return item_name
def setData(value):
	global item_name
	#print("set val = "+value)
	item_name = str(value)

def detect_barcode():
	# grab global references to the video stream, output frame, and
	# lock variables
	global vs, outputFrame, lock

	# initialize the motion detector and the total number of frames
	# read thus far
	BD = BarcodeDetector()

	# loop over frames from the video stream
	while True:
		# read the next frame from the video stream, resize it,
		# convert the frame to grayscale, and blur it
		frame = vs.read()
		frame = imutils.resize(frame, width=400)

		# grab the current timestamp and draw it on the frame
		timestamp = datetime.datetime.now()
		cv2.putText(frame, timestamp.strftime(
			"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 0, 255), 1)

		try:
			#print("item_name= "+getData())
			result = BD.detect(frame)
			if result is not None:
				#print("result = "+result)
				setData(result)

		except IndexError:
			pass
		# acquire the lock, set the output frame, and release the
		# lock

		with lock:
			outputFrame = frame.copy()

def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock

	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue

			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

			# ensure the frame was successfully encoded
			if not flag:
				continue

		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
			bytearray(encodedImage) + b'\r\n')



@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

# start a thread that will perform motion detection
t = threading.Thread(target=detect_barcode)
t.daemon = True
t.start()
# start the flask App
app.run(host='0.0.0.0', port=5000, debug=True, threaded=True, use_reloader=False)
