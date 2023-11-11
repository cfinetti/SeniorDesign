import numpy as np
import cv2 as cv
from update import send_decrease, send_increase

def car_entered():
    if send_increase():
        print "Increased capacity successfully."
    else:
        print "Failed to increase capacity."

def car_exited():
    if send_decrease():
        print "Decreased capacity successfully."
    else:
        print "Failed to decrease capacity or capacity is already zero."

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print "Cannot open camera"
    exit()
cur_frame, prev_frame = None, None

mog = cv.BackgroundSubtractorMOG2()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print "Can't receive frame (stream end?). Exiting ..."
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

    # Find contours
    contours, _ = cv.findContours(fgmask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Ignore small contours
        if cv.contourArea(contour) < 1000:
            continue

        # Draw bounding box around contour
        x, y, w, h = cv.boundingRect(contour)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv.imshow('Motion Detection', frame)
    # Display the resulting frame

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
