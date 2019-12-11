import numpy as np
import cv2

def cam():
    cap = cv2.VideoCapture(0)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        color = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        # Display the resulting frame
        cv2.imshow('frame', color)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.imwrite('test.jpeg', gray)
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
