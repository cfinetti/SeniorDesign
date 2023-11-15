import numpy as np
import cv2 as cv
from update import send_decrease, send_increase

def car_entered():
    if send_decrease():
        print("Decreased availability successfully.")
    else:
        print("Failed to decrease availability.")

def car_exited():
    if send_decrease():
        print("Increased availability successfully.")
    else:
        print("Failed to increase availability.")

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
cur_frame, prev_frame = None, None
motion_detected = False

mog = cv.createBackgroundSubtractorMOG2()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    cur_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cur_frame = cv.GaussianBlur(cur_frame, (21, 21), 0)
    if prev_frame is None:
        prev_frame = cur_frame
        continue
    fgmask = mog.apply(cur_frame)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    fgmask = cv.erode(fgmask, kernel, iterations=1)
    fgmask = cv.dilate(fgmask, kernel, iterations=1)

    contours, hierarchy = cv.findContours(fgmask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Ignore small contours
        if cv.contourArea(contour) < 1000:
            continue

        # Draw bounding box around contour
        x, y, w, h = cv.boundingRect(contour)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv.imshow('Motion Detection', frame)
    # Display the resulting frame

    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()