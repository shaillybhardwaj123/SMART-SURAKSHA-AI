import os
import werkzeug.serving

# Monkeypatch werkzeug.serving to force Flask run on 0.0.0.0 and dynamic port
original_run_simple = werkzeug.serving.run_simple
def patched_run_simple(hostname, port, application, *args, **kwargs):
    env_port = os.environ.get('PORT')
    if env_port:
        port = int(env_port)
    hostname = '0.0.0.0'
    return original_run_simple(hostname, port, application, *args, **kwargs)
werkzeug.serving.run_simple = patched_run_simple

from flask import Flask, render_template, request, jsonify
from accident_model import predict_risk
from ml_module import get_ml_module

app = Flask(__name__)

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

@app.route('/get_iot_status')
def get_iot_status():
    """Returns demo/default IoT status (no Arduino on server)."""
    return jsonify({
        "status":                "disconnected",
        "distance":              999,
        "speed":                 0,
        "collision":             False,
        "collision_probability": 0.0,
        "risk":                  "LOW"
    })

@app.route('/start_camera', methods=['POST'])
def start_camera():
    """Camera not available on cloud — returns stub response."""
    return jsonify({'status': 'not_available', 'message': 'Camera not supported on cloud deployment'})

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    return jsonify({'status': 'stopped'})

@app.route('/get_status')
def get_status():
    return jsonify({'status': 'ACTIVE'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
