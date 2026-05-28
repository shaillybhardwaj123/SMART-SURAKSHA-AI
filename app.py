from flask import Flask, render_template, request, jsonify
from accident_model import predict_risk
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_risk', methods=['POST'])
def check_risk():
    data = request.get_json() or {}
    speed = data.get('speed')
    weather = data.get('weather')
    result = predict_risk(speed, weather)
    return jsonify({'result': result})

@app.route('/get_iot_status')
def get_iot_status():
    return jsonify({
        "status": "disconnected",
        "distance": 999,
        "speed": 0,
        "collision": False,
        "collision_probability": 0.0,
        "risk": "LOW"
    })

@app.route('/start_camera', methods=['POST'])
def start_camera():
    return jsonify({'status': 'not_available'})

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    return jsonify({'status': 'stopped'})

@app.route('/get_status')
def get_status():
    return jsonify({'status': 'ACTIVE'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
