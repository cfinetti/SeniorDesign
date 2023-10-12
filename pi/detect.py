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
import cv2
import tensorflow as tf


class CarDetector:
    def __init__(self, model_path):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def detect(self, image):
        # Preprocess the image
        input_tensor = cv2.resize(image, (self.input_details[0]['shape'][2], self.input_details[0]['shape'][1]))
        input_tensor = input_tensor.astype(np.uint8)
        input_tensor = np.expand_dims(input_tensor, axis=0)

        # Run inference
        self.interpreter.set_tensor(self.input_details[0]['index'], input_tensor)
        self.interpreter.invoke()

        # Extract output data
        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        class_ids = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]

        return boxes, class_ids, scores

    def draw_boxes(self, image, boxes, class_ids, scores, threshold=0.5):
        height, width, _ = image.shape
        for i in range(len(scores)):
            if scores[i] > threshold:  # assuming class '3' is for cars
                box = boxes[i]
                y1, x1, y2, x2 = int(box[0] * height), int(box[1] * width), int(box[2] * height), int(box[3] * width)
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return image


def main(model_path):
    cap = cv2.VideoCapture(0)  # Use the default camera
    detector = CarDetector(model_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        boxes, class_ids, scores = detector.detect(frame)
        frame = detector.draw_boxes(frame, boxes, class_ids, scores, threshold=0.5)

        cv2.imshow('Car Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    model_path = "models/lite-model_efficientdet_lite0_detection_default_1.tflite"
    main(model_path)
