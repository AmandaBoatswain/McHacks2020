# McHacks2020 - I Better Munch'it!

For the McHacks hackathon, we developed a food waste reducer which keeps track of the grocery items you keep in your fridge. Every time you buy an item, your fridge scans its UPC code, grabs the item's name, stores the data, and automatically notifies you when it's nearing its expiration date.

We developed a bar code and food scanner in python using OpenCV, pyzbar and sklearn. The bar codes were detected using image processing (code taken from https://www.pyimagesearch.com/2014/12/15/real-time-barcode-detection-video-python-opencv/), and were decoded using a database to get the names of the items and add them to the fridge queue. Following this, a web application in JavaScript and HTML were created to display the items in the fridge and keep track of their expiration dates. Items enter and leave the fridge all throughout the day, so we created a dynamic mySQL database and linked it with our python code using Flask. The video feed from the webcam scanner is also streamed to the website using flask, giving to a complete and easy to use app that is accessible from multiple platforms.

Python Environment

To run this code, you need to have a version of python 3 up and running.This code was tested using python version 3.6.8. Python libraries imutils, pyzbar, cv2, flask and sqlalchemy must be installed. 

TO RUN

Download all the files from the zip folder.
Open a terminal and cd to the project folder.
Run $ python grocery_web_app.py to start the program.
Go to: http://localhost:5000/ and test the app! 

More info on this app and its contributors can be found on our devpost page: https://devpost.com/software/i-better-munch-it-ibm

![App Interface(https://github.com/AmandaBoatswain/McHacks2020/blob/master/App%20interface.png)

![App Database(https://github.com/AmandaBoatswain/McHacks2020/blob/master/App%20database.png)
