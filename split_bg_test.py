import cv2

def split(img):
    h, w, channels = img.shape
 
    half = w//2
    left_part = img[:, :half] 
    right_part = img[:, half:]  
    return left_part, right_part

def main():
    #1
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    #2
    while ret:
        ret, frame = camera.read()
        left, right = split(frame)
        cv2.imshow('left', left)
        cv2.imshow('right', right)
        key = cv2.waitKey(1)
        if key == ord("Q") or key == ord("q") or key == 27:
            break
    #3
    camera.release()
    cv2.destroyAllWindows()
#4
if __name__ == '__main__':
    main()