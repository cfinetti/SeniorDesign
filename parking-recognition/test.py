import cv2
from picamera2 import Picamera2
cap = cv2.VideoCapture(0)

picam2 = Picamera2()
config = picam2.create_preview_configuration()
picam2.configure(config)
picam2.start()
if not cap.isOpened():
	raise IOError("Cannot open camera")
	
while True:
	frame = picam2.capture_array()
	cv2.imshow('Input', frame)
	if cv2.waitkey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
