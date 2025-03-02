# CODE TAKEN FROM https://pythonslearning.com/2021/04/how-to-build-real-time-opencv-barcode-reader-or-scanner-using-python.html
# note: make it so that it closes and writes to file after finding one barcode that has information
#import libraries
import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import openfoodfacts
import json
import pymysql


api = openfoodfacts.API(user_agent="MyAwesomeApp/1.0")

dataset = openfoodfacts.ProductDataset(dataset_type="csv")

def detect_and_decode_barcode(image):
    breaking = False
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect barcodes in the grayscale image
    barcodes = decode(gray)

    # Loop over detected barcodes
    for barcode in barcodes:
        # Extract barcode data and type
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type

        # Print barcode data and type
        print("Barcode Data:", barcode_data)
        print("Barcode Type:", barcode_type)
        
        data = api.product.get(str(barcode_data))
        push_to_db(json.dumps(data))
        breaking = True


    return image, breaking

def push_to_db(text):
    try:
        connection = pymysql.connect(
            host="192.168.0.131",
            user="root",
            password="password",
            database="fridgefinds",
            charset='utf8mb4',
        )
        cur = connection.cursor()
        sql = """insert into `Items` (iteminfo) values (%s)"""
        cur.execute(sql,(text))
        connection.commit()
        print("ADDED", text ,"TO DB!")
        connection.close()
    except pymysql.err.OperationalError as e:
        print(f"MySQL connection failed: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
#The main function will turn on the video camera of the computer, and the then call the decoding function. Here is the code:
def main():
    #1
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    breaking = False
    #2
    while ret and (breaking == False):
        ret, frame = camera.read()
        frame, breaking = detect_and_decode_barcode(frame)
        cv2.imshow('Barcode/QR code reader', frame)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break
    #3
    camera.release()
    cv2.destroyAllWindows()
#4
if __name__ == '__main__':
    main()