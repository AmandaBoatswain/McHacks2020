# McWics Hackathon project

# import the necessary packages
from pyzbar import pyzbar
import datetime
import imutils
import time
import cv2
import pandas


# path to the database
grocery_path = "Grocery_UPC_Database.csv"

# import grocery list database
grocery_df = pandas.read_csv(grocery_path)

print("[INFO] Importing grocery database...")
headers = list(grocery_df.columns)

class BarcodeDetector:
    def __init__(self):
        # create an empty set to store the detected bar codes
        self.found = set()

        # create an empty list to store the item names
        self.grocery_list = []

    def detect(self, image):
        # scan the image for barcodes
        barcodes = pyzbar.decode(image)

        # loop over the detected barcodes
        for barcode in barcodes:
            # extract the bounding box location of the barcode and draw
            # the bounding box surrounding the barcode on the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # the barcode data is a bytes object so if we want to draw it
            # on our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            #print("BarCode", barcodeData)

            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            if barcodeData not in self.found:
                # if the barcode text is currently not in our CSV file, write
                # the timestamp + barcode to disk and update the set
                try:
                    result = grocery_df.loc[grocery_df[headers[0]] == int(barcodeData)]
                    result = result.iloc[0]["name"]
                    #print("Final result: ", result)
                    return result

                except ValueError:
                    pass
