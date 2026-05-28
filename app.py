from flask import Flask, render_template, request, jsonify
from accident_model import predict_risk
from drowsiness import start_drowsiness
from ml_module import get_ml_module
import threading
import os
import json

app = Flask(__name__)

drowsy_thread  = None
drowsy_running = False

# ML model startup pe load karo
ml_model = get_ml_module()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_risk', methods=['POST'])
def check_risk():
    data    = request.get_json()
    speed   = data.get('speed')
    weather = data.get('weather')
    result  = predict_risk(speed, weather)
    return jsonify({'result': result})

@app.route('/predict/iot', methods=['POST'])
def predict_iot():
    data     = request.get_json()
    speed    = float(data.get('speed', 0))
    distance = float(data.get('distance', 999))
    weather  = data.get('weather', 'clear')

    risk = predict_risk(speed, weather)
    collision, prob = ml_model.predict_collision(speed, distance)

    if distance < 30:
        collision = True
        risk = "HIGH"

    return jsonify({
        'risk':                  risk,
        'collision':             collision,
        'collision_probability': prob,
        'speed':                 speed,
        'distance':              distance
    })

# ── Frontend ke liye live Arduino data ─────────────────────
@app.route('/get_iot_status')
def get_iot_status():
    """
    arduino_bridge.py → arduino_data.json likhta hai
    Ye route woh file padhke frontend ko deta hai
    """
    DATA_FILE = "arduino_data.json"
    try:
        if not os.path.exists(DATA_FILE):
            return jsonify({
                "status":                "disconnected",
                "distance":              999,
                "speed":                 0,
                "collision":             False,
                "collision_probability": 0.0,
                "risk":                  "LOW"
            })

        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── Drowsiness routes ───────────────────────────────────────
@app.route('/start_camera', methods=['POST'])
def start_camera():
    global drowsy_thread, drowsy_running
    if drowsy_running:
        return jsonify({'status': 'already_running'})
    drowsy_running = True

    def run_drowsy():
        global drowsy_running
        try:
            start_drowsiness()
        except Exception as e:
            print(f"Drowsiness error: {e}")
        finally:
            drowsy_running = False

    drowsy_thread = threading.Thread(target=run_drowsy, daemon=True)
    drowsy_thread.start()
    return jsonify({'status': 'started'})

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    global drowsy_running, drowsy_thread
    drowsy_running = False
    if drowsy_thread:
        drowsy_thread.join(timeout=2)
    return jsonify({'status': 'stopped'})

@app.route('/get_status')
def get_status():
    if os.path.exists('status.txt'):
        with open('status.txt', 'r') as f:
            status = f.read().strip()
        return jsonify({'status': status})
    return jsonify({'status': 'ACTIVE'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)