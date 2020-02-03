# McHacks2020 - I Better Munch'it!
Code developed for a food waste reducer which keeps track of the grocery items you keep in your fridge. Every time you buy an item, your fridge scans its UPC code, grabs the item's name, stores the data, and automatically notifies you when it's nearing its expiration date.

We developed a bar code and food scanner in python using OpenCV, pyzbar and sklearn. The bar codes were detected using image processing (code taken from https://www.pyimagesearch.com/2014/12/15/real-time-barcode-detection-video-python-opencv/), and were decoded using a database to get the names of the items and add them to the fridge queue. Following this, a web application in JavaScript and HTML was created to display the items in the fridge and keep track of their expiration dates. Items enter and leave the fridge all throughout the day, so we created a dynamic mySQL database and linked it with our python code using Flask. The video feed from the webcam scanner is also streamed to the website using flask, giving to a complete and easy to use app that is accessible from multiple platforms.


