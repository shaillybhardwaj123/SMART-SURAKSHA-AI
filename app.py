from flask import Flask, render_template, Response, jsonify
import cv2
import threading
import random
import numpy as np

from ai_module import AIModule
from iot_module import IoTModule
from ml_module import MLModule

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

print("Initializing AI Crash Detectors...")
ai = AIModule()
iot = IoTModule()
ml = MLModule()

camera = cv2.VideoCapture(0)

def generate_frames():
    global ai, camera
    while True:
        if not camera.isOpened():
            camera.open(0)
            
        success, frame = camera.read()
        if not success:
            # Create a black error frame instead of breaking the connection route entirely
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "CAMERA ERROR - Retrying...", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            cv2.waitKey(1000) # wait 1s before retry
            continue
            
        processed_frame, max_conf = ai.process_frame(frame)
        
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/status')
def get_status():
    global ai, iot, ml
    
    # 1. IoT Hardware Data
    dist, force = iot.get_sensor_data()
    
    # 2. AI Video Data
    ai_conf = ai.latest_collision_confidence
    cars_dist = ai.min_distance_between_cars
    
    # 3. Random speed generator (simulation)
    speed = random.randint(40, 110)
    
    # 4. Predict Collision with ML
    accident_occured, prob = ml.predict_accident(speed, cars_dist, force, ai_conf)
    
    action_taken = "SAFE"
    if accident_occured:
        iot.trigger_crash_alarm()
        action_taken = "CRASH DETECTED"
    else:
        iot.reset_alarm()
            
    return jsonify({
        "speed": f"{speed} km/h",
        "impact_force": f"{force}G",
        "cam_distance": f"{cars_dist:.1f}px",
        "ai_confidence": f"{ai_conf * 100:.1f}%",
        "ml_probability": f"{prob * 100:.1f}%",
        "crash": accident_occured,
        "action": action_taken
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
