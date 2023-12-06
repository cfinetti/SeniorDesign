import cv2
import numpy as np
import platform
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


class VehicleTracker:
    def __init__(self):
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=70)
        self.active_vehicles = {}  # Stores ID and last known position
        self.next_vehicle_id = 1
        self.line_position = 320  # Adjust based on your video feed
        self.id_positions = {}  # Stores positions of vehicles across frames

    def process_frame(self, frame):
        fg_mask = self.background_subtractor.apply(frame)
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        current_centroids = self.extract_centroids(contours, frame)
        self.update_vehicles(current_centroids, frame)

        # Drawing the line
        cv2.line(frame, (self.line_position, 0), (self.line_position, frame.shape[0]), (255, 0, 0), 2)

        return frame

    def extract_centroids(self, contours, frame):
        centroids = []
        for contour in contours:
            if cv2.contourArea(contour) > 3000:  # Threshold for vehicle size
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw bounding box
                centroids.append((x + w // 2, y + h // 2))
        return centroids

    def update_vehicles(self, centroids, frame):
        for centroid in centroids:
            matched_id = self.match_vehicle(centroid)
            if matched_id is None:
                self.active_vehicles[self.next_vehicle_id] = centroid
                self.id_positions[self.next_vehicle_id] = [centroid]
                self.next_vehicle_id += 1
            else:
                self.active_vehicles[matched_id] = centroid
                self.id_positions[matched_id].append(centroid)
                self.check_direction(matched_id, frame)

    def match_vehicle(self, centroid):
        for vehicle_id, position in self.active_vehicles.items():
            if np.linalg.norm(np.array(position) - np.array(centroid)) < 100:  # Matching threshold
                return vehicle_id
        return None

    def check_direction(self, vehicle_id, frame):
        positions = self.id_positions[vehicle_id]
        if len(positions) < 2:
            return

        prev_x, prev_y = positions[-2]
        curr_x, curr_y = positions[-1]

        # Check if the vehicle has crossed the line since the last frame
        if prev_x < self.line_position <= curr_x:
            print(f"Vehicle ID {vehicle_id} entered.")
        elif prev_x > self.line_position >= curr_x:
            print(f"Vehicle ID {vehicle_id} exited.")
            self.active_vehicles.r

        # Draw the centroid and ID
        cv2.circle(frame, (curr_x, curr_y), 5, (0, 0, 255), -1)
        cv2.putText(frame, f'ID: {vehicle_id}', (curr_x - 10, curr_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Initialize the video capture and vehicle tracker
on_linux = platform.system() == 'Linux'
cc = cv2.VideoWriter_fourcc(*'XVID')
file = cv2.VideoWriter('output.avi', cc, 15.0, (640, 480))
if on_linux:
    from picamera2 import Picamera2
    piCam = Picamera2()
    config = piCam.create_preview_configuration(main={"size": (3280, 2464), "format": "RGB888"},
                                                lores={"size": (640, 480), "format": "YUV420"})

    piCam.preview_configuration.main.size=(640, 480)
    piCam.preview_configuration.main.format="RGB888"
    piCam.preview_configuration.align()
    piCam.configure("preview")
    piCam.start()
else:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

tracker = VehicleTracker()

while True:
    if on_linux:
        frame = piCam.capture_array("lores")
    else :
        ret, frame = cap.read()
    processed_frame = tracker.process_frame(frame)
    cv2.imshow("Parking Lot Monitoring", processed_frame)
    file.write(processed_frame);
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
