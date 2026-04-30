<div align="center">

# 🚨 Smart-Suraksha

### AI-Powered Road Accident Detection & Emergency Alert System

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Arduino](https://img.shields.io/badge/Arduino-UNO-00979D?style=flat-square&logo=arduino&logoColor=white)](https://arduino.cc)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-Vision-5C3EE8?style=flat-square&logo=opencv&logoColor=white)](https://opencv.org)
[![License](https://img.shields.io/badge/License-Academic-green?style=flat-square)](LICENSE)

*Real-time accident detection using Computer Vision, Machine Learning, and IoT — because every second counts.*

[Overview](#-overview) · [Architecture](#-architecture) · [Modules](#-modules) · [Getting Started](#-getting-started) · [API Reference](#-api-reference) · [Team](#-team)

</div>

---

## 🎯 Overview

**Smart-Suraksha** is an integrated safety system designed to detect road accidents and trigger emergency alerts in real time. It bridges the gap between the moment an accident occurs and emergency response by combining AI-driven computer vision, a trained machine learning model, and physical IoT sensors — all orchestrated through a live web dashboard.

**The core problem it solves:** Accidents often go undetected for critical minutes, delaying life-saving response. Smart-Suraksha automates detection and alerting the moment risk is identified.

### Key Capabilities

- 🎥 **Drowsiness Detection** — CNN model monitors driver alertness via webcam in real time
- 📡 **Obstacle & Speed Sensing** — Arduino-based hardware reads distance and velocity from physical sensors
- 🧠 **Risk Prediction** — Logistic Regression model classifies risk as HIGH / MEDIUM / LOW
- 🌐 **Live Web Dashboard** — Flask-powered frontend for monitoring and manual override
- 🔊 **Voice & Hardware Alerts** — Instant spoken warnings and LED/buzzer responses
- ☁️ **Emergency Notifications** — SMS/Email alerts and Firebase logging on HIGH risk events

---

## 🏗 Architecture

```
┌─────────────────┐    ┌──────────────────────┐    ┌─────────────────────┐
│   Webcam Feed   │───▶│  Drowsiness Detection │    │  Weather API (Live) │
└─────────────────┘    │  (CNN + OpenCV)       │    └──────────┬──────────┘
                       └──────────┬───────────┘               │
┌─────────────────┐               │                           │
│ HC-SR04 Sensor  │───▶           │                           │
│ Hall Effect     │    ┌──────────▼───────────────────────────▼──────────┐
│ (Arduino UNO)   │───▶│         Flask REST API + ML Engine              │
└─────────────────┘    │       (Risk Prediction: HIGH / MEDIUM / LOW)    │
                       └──────────┬──────────────────────────────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
      ┌───────────────┐  ┌──────────────┐  ┌──────────────────┐
      │ Web Dashboard │  │ Voice Alert  │  │ SMS/Email/Firebase│
      │  (HTML/CSS/JS)│  │  (pyttsx3)   │  │   Notifications  │
      └───────────────┘  └──────────────┘  └──────────────────┘
```

---

## 📦 Modules

### Module 1 — Computer Vision (AI)
Detects driver drowsiness in real time using the live webcam feed.

| Item | Detail |
|------|--------|
| Stack | Python, OpenCV, CNN |
| Input | Webcam stream |
| Output | Drowsiness flag → Flask API |

---

### Module 2 — IoT (Arduino UNO)
Reads physical sensor data and triggers onboard hardware alerts (LEDs, buzzer).

| Item | Detail |
|------|--------|
| Stack | Arduino UNO, HC-SR04, Hall Effect Sensor |
| Input | Obstacle distance, wheel speed |
| Output | Serial data → Python bridge → ML model |

---

### Module 3 — Machine Learning (Risk Engine)
A Logistic Regression model trained on real traffic accident data classifies current driving conditions.

| Item | Detail |
|------|--------|
| Stack | Python, Scikit-Learn, Pandas |
| Input | Speed, weather conditions, obstacle distance |
| Output | `HIGH` / `MEDIUM` / `LOW` risk label |

---

### Module 4 — Web Dashboard (Frontend)
A Flask-served live dashboard that accepts both manual input and live IoT sensor data.

| Item | Detail |
|------|--------|
| Stack | Flask, HTML, CSS, JavaScript |
| Features | Manual input form, IoT simulation tab, live risk display |

---

### Module 5 — Integration Layer
Connects all modules through a unified Flask REST API with voice alerts and external notifications.

| Item | Detail |
|------|--------|
| Stack | Flask, pyttsx3, pyserial, Firebase |
| Handles | Serial bridging, alert routing, DB logging |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.8+ |
| ML Model | Scikit-Learn — Logistic Regression |
| Computer Vision | OpenCV + CNN |
| Backend | Flask, Flask-CORS |
| IoT Controller | Arduino UNO |
| Sensors | HC-SR04 Ultrasonic, Hall Effect |
| Voice Alerts | pyttsx3 |
| Serial Comm | pyserial |
| Frontend | HTML, CSS, JavaScript |
| Database | Firebase |
| Notifications | SMS / Email API |

---

## 🔧 Hardware Requirements

| Component | Qty | Purpose |
|-----------|:---:|---------|
| Arduino UNO | 1 | Main microcontroller |
| HC-SR04 Ultrasonic Sensor | 1 | Obstacle distance measurement |
| Hall Effect Sensor | 1 | Wheel speed (km/h) |
| Buzzer | 1 | Onboard audio alert |
| Red LED | 1 | HIGH RISK indicator |
| Yellow LED | 1 | MEDIUM RISK indicator |
| Green LED | 1 | SAFE indicator |
| 220Ω Resistors | 3 | LED current protection |
| USB Cable (Type-B) | 1 | Arduino ↔ PC communication |
| Jumper Wires | — | Circuit connections |
| Breadboard | 1 | Circuit prototyping |
| Webcam | 1 | Drowsiness detection |

---

## 📁 Project Structure

```
Smart-Suraksha/
│
├── ml_model/
│   ├── train_model.py                          # Model training script
│   ├── risk_model.pkl                          # Trained Logistic Regression model
│   ├── scaler.pkl                              # StandardScaler (preprocessing)
│   └── dataset_traffic_accident_prediction1.csv
│
├── ai_module/
│   ├── drowsiness.py                           # CNN-based drowsiness detection
│   └── haarcascade_eye.xml                     # Haar cascade for eye detection
│
├── iot_module/
│   └── arduino_sensors.ino                     # Arduino firmware (sensors + alerts)
│
├── backend/
│   ├── app_final.py                            # Flask API + ML integration
│   └── serial_bridge_voice.py                 # Arduino bridge + voice alerts
│
├── frontend/
│   └── frontend_final.html                     # Web dashboard
│
├── requirements.txt
└── README.md
```

---

## ⚡ Getting Started

### Prerequisites

- Python 3.8+
- Arduino IDE
- A webcam
- Arduino UNO with components wired (see [pin connections](#-arduino-pin-connections))

### 1. Clone the Repository

```bash
git clone https://github.com/UchitAgrawal/Smart-Suraksha.git
cd Smart-Suraksha
```

### 2. Install Python Dependencies

```bash
pip install flask flask-cors scikit-learn pandas numpy opencv-python pyttsx3 pyserial requests
```

### 3. Upload Arduino Firmware

1. Open `iot_module/arduino_sensors.ino` in the Arduino IDE
2. Select **Tools → Board → Arduino UNO**
3. Select **Tools → Port → COM3** *(or your system's port)*
4. Click **Upload**

---

## ▶️ Running the System

The system runs in three parallel processes. Open a terminal for each.

**Terminal 1 — Start the Flask Backend**

```bash
cd backend
python app_final.py
```

Expected output:
```
✅ ML Model Trained Successfully!
 * Running on http://0.0.0.0:5000
```

**Terminal 2 — Start the Arduino Bridge**

```bash
cd backend
python serial_bridge_voice.py
```

Expected output:
```
✅ Arduino connected on COM3
🚀 Listening to Arduino...
✅ Arduino ready!
```

> **Note:** Update the serial port in `serial_bridge_voice.py` (line 12) to match your system:
> ```python
> SERIAL_PORT = 'COM3'           # Windows
> SERIAL_PORT = '/dev/ttyUSB0'  # Linux / macOS
> ```

**Step 3 — Open the Dashboard**

Open `frontend/frontend_final.html` in any browser.

- Use the **Manual Input** tab to test with custom speed and weather values
- Use the **IoT Sensor** tab to simulate or view live Arduino data

---

## 🔌 Arduino Pin Connections

```
Arduino UNO
│
├── Pin 2  ──▶  Hall Effect Sensor  (Signal / OUT)
├── Pin 3  ──▶  HC-SR04             (TRIG)
├── Pin 4  ──▶  HC-SR04             (ECHO)
├── Pin 8  ──▶  Buzzer              (+)
├── Pin 9  ──▶  Red LED             (+ via 220Ω resistor)
├── Pin 10 ──▶  Yellow LED          (+ via 220Ω resistor)
├── Pin 11 ──▶  Green LED           (+ via 220Ω resistor)
├── 5V     ──▶  HC-SR04 VCC, Hall Sensor VCC
└── GND    ──▶  All GND connections
```

---

## 🌐 API Reference

| Method | Endpoint | Description | Payload |
|--------|----------|-------------|---------|
| `POST` | `/predict/manual` | Risk prediction from frontend form | `{ speed, weather }` |
| `POST` | `/predict/iot` | Risk prediction from Arduino sensors | `{ speed, weather, device_id }` |
| `GET` | `/health` | Server health check | — |

### Example Request

```bash
curl -X POST http://localhost:5000/predict/manual \
  -H "Content-Type: application/json" \
  -d '{"speed": 85, "weather": "rain"}'
```

### Example Response

```json
{
  "risk": "HIGH",
  "message": "⚠️ HIGH ACCIDENT RISK — Alert Sent!",
  "speed": 85,
  "weather": "rain",
  "source": "frontend"
}
```

---

## 🔊 Voice Alert Reference

| Trigger | Voice Output |
|---------|-------------|
| System start | *"Smart-Suraksha system started. Monitoring road conditions."* |
| HIGH risk | *"Warning! High accident risk detected. Speed is X km/h. Obstacle at Y cm. Please slow down immediately!"* |
| MEDIUM risk | *"Caution! Medium risk detected. Speed is X km/h. Please drive carefully."* |
| LOW risk | *"Conditions are safe. Drive carefully."* |

---

## 👥 Team

| Member | Responsibility |
|--------|----------------|
| Member 1 | Module 1 — AI / Computer Vision (CNN + OpenCV) |
| Member 2 | Module 2 — IoT (Arduino + Sensors) |
| Member 3 | Module 3 — Machine Learning (Logistic Regression) |
| Member 4 | Module 4 — Frontend (Flask + HTML/CSS/JS) |
| All Members | Module 5 — System Integration |

---

## 📄 License

This project was developed for academic purposes as part of a college mini-project submission. It is not licensed for commercial use.

---

<div align="center">

Built with ❤️ by **Team Smart-Suraksha**

*If this project helped you, consider giving it a ⭐*

</div>
