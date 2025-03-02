import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import openfoodfacts
import json
api = openfoodfacts.API(user_agent="MyAwesomeApp/1.0")
def split(img):
    h, w, channels = img.shape
 
    half = w//2
    left_part = img[:, :half] 
    right_part = img[:, half:]  
    return left_part, right_part

def get_areas(frame, side):
    #frame = cv2.flip(frame,1)
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgbg = cv2.createBackgroundSubtractorMOG2(128,cv2.THRESH_BINARY,1)
    masked_image = fgbg.apply(gray_image)
    masked_image[masked_image==127]=0
    ret, thresh = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
    
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    area = 0
    for c in cnts:
        area += cv2.contourArea(c)
        cv2.drawContours(thresh,[c], 0, (0,0,0), 2)
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    #print(area)
    outtext = "Area: " + str(area)
    limit = 100000/2 # for testing purpose
    if area > limit:  # this means that the background is greater than limit 
        cv2.putText(frame, outtext, (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
        print(side, "is empty")
    else:
        cv2.putText(frame, outtext, (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1, (225, 0, 255), 1, cv2.LINE_AA)
# Displaying the output image
    return frame, side

def detect_and_decode_barcode(image, side):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect barcodes in the grayscale image
    barcodes = decode(gray)

    # Loop over detected barcodes
    for barcode in barcodes:
        # Extract barcode data and type
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type

        # Print barcode data and type
        print("Side:",side, "Barcode Data:", barcode_data)
        print("Side:",side,"Barcode Type:", barcode_type)
        
        #data = api.product.get(str(barcode_data))
        #data = api.product.get("3017620422003")
        #with open("jsonout.json", "w") as fp:
            #json.dump(data , fp)

        # Draw a rectangle around the barcode
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Put barcode data and type on the image
        cv2.putText(image, f"{barcode_data} ({barcode_type})",
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    return image, side

def main():
    #1
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    #2
    while ret:
        ret, frame = camera.read()
        left, right = split(frame)
        left, ls = get_areas(left, "left")
        right, rs = get_areas(right, "right")
        left, ls = detect_and_decode_barcode(left, "left")
        right, rs = detect_and_decode_barcode(right, "right")
        cv2.imshow(ls, left)
        cv2.imshow(rs, right)
        key = cv2.waitKey(1)
        if key == ord("Q") or key == ord("q") or key == 27:
            break
    #3
    camera.release()
    cv2.destroyAllWindows()
#4
if __name__ == '__main__':
    main()