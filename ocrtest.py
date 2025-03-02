import cv2
import pytesseract
from dateutil.parser import *
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pymysql

pytesseract.pytesseract.tesseract_cmd =  "C:\\Users\\maxin\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"
 
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
 
def check_date(text):
    check = text.split()
    for i in check:
        found = re.findall("[0-9][0-9]/[0-1][0-9]/[0-9][0-9]",i)
        if found:
            try:
                out = parse(i, fuzzy=True)
                if (out > datetime.now()) and (out < (datetime.now() + relativedelta(years=1))):
                    return out
            except:
                pass
            

def do_ocr(frame):
    breaking = False
    text = pytesseract.image_to_string(frame)
    if text != "":
        getdate = check_date(text)
        if getdate != None:
            print(getdate)
            push_to_db(getdate)
            breaking = True
    return frame, breaking

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

        sql = """insert into `dates` (date) values (%s)"""
        cur.execute(sql,(text))
        connection.commit()
        print("ADDED TO DB!")
        connection.close()
    except pymysql.err.OperationalError as e:
        print(f"MySQL connection failed: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    

breaking = False
while (breaking == False):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame, breaking = do_ocr(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()