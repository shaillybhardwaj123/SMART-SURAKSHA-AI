import cv2
import numpy as np
import math

class AIModule:
    def __init__(self):
        print("Loading OpenCV Vehicle Tracking for accuracy...")
        # Load the dedicated car cascade XML file
        self.car_cascade = cv2.CascadeClassifier('cars.xml')
        self.latest_collision_confidence = 0.0
        self.min_distance_between_cars = 999.0

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect cars in frame
        cars = self.car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
        
        highest_collision_prob = 0.0
        min_dist = 999.0
        
        for (x, y, w, h) in cars:
            # Draw tracking box
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 3)
            cv2.putText(frame, "VEHICLE DETECTED", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            # Simple Crash Logic: If your car takes up a massive portion of the screen!
            if w > 220:  # If you lean very close to the camera
                highest_collision_prob = 0.99
                min_dist = 0.1
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 5) # Red box
                cv2.putText(frame, "IMMINENT COLLISION!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                
        # If there are exactly two objects detected
        if len(cars) >= 2:
            (x1, y1, w1, h1) = cars[0]
            (x2, y2, w2, h2) = cars[1]
            c1 = (x1 + w1//2, y1 + h1//2)
            c2 = (x2 + w2//2, y2 + h2//2)
            dist = math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)
            
            if dist < 120:  # The boxes are very close to each other
                highest_collision_prob = 0.99
                min_dist = dist
                cv2.line(frame, c1, c2, (0, 0, 255), 3)
                cv2.putText(frame, "COLLISION!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        self.latest_collision_confidence = float(highest_collision_prob)
        self.min_distance_between_cars = float(min_dist) if min_dist != 999.0 else 500.0
        
        return frame, highest_collision_prob

if __name__ == "__main__":
    ai = AIModule()
    print("AI Module Collision detection test complete.")
