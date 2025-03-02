import cv2

def main():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    while ret:
        ret, frame = camera.read()
        cv2.imshow('areatest', frame)
        key = cv2.waitKey(1)
        if key == ord("Q") or key == ord("q") or key == 27:
            break
    camera.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main()