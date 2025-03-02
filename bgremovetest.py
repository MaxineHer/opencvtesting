# CODE TAKEN FROM https://pythonslearning.com/2021/04/how-to-build-real-time-opencv-barcode-reader-or-scanner-using-python.html

#import libraries
import cv2
#Now, let’s write the function. Instead of adding part by part, I will share the whole function with you. Since, indentation matters when writing in python, I don’t want to disorganize things by ruining the structure of the code. I will add my comments below the code.
def get_areas(frame):
    frame = cv2.flip(frame,1)
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
    limit = 100000 # for testing purpose
    if area > limit:  # this means that the background is greater than limit 
        cv2.putText(frame, outtext, (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
    else:
        cv2.putText(frame, outtext, (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1, (225, 0, 255), 1, cv2.LINE_AA)
# Displaying the output image
    return frame

def get_thresh(frame):
    frame = cv2.flip(frame,1)
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
        cv2.rectangle(thresh,(x,y),(x+w,y+h),(0,0,0),2)
    #print(area)
    outtext = "Area: " + str(area)
    limit = 100000 # for testing purpose
    if area > limit:  # this means that the background is greater than limit 
        cv2.putText(thresh, outtext, (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
    else:
        cv2.putText(thresh, outtext, (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
    return thresh

#The main function will turn on the video camera of the computer, and the then call the decoding function. Here is the code:
def main():
    #1
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    #2
    while ret:
        ret, frame = camera.read()
        frame = get_thresh(frame)
        cv2.imshow('areatest', frame)
        key = cv2.waitKey(1)
        if key == ord("Q") or key == ord("q") or key == 27:
            break
    #3
    camera.release()
    cv2.destroyAllWindows()
#4
if __name__ == '__main__':
    main()