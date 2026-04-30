from flask import Flask, render_template, request
from accident_model import predict_risk   # 👉 ML SAME
import subprocess
import os

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    result = ""

    if request.method == 'POST':
        speed = request.form.get('speed')
        weather = request.form.get('weather')

        if speed and speed.strip() != "":
            speed = int(speed)

            # 🔴 ML PART (UNCHANGED)
            result = predict_risk(speed, weather)

            # 🔴 ADD (READ DROWSINESS STATUS)
            try:
                with open("status.txt", "r") as f:
                    driver_status = f.read().strip()
            except:
                driver_status = "ACTIVE"

            if driver_status == "DROWSY":
                result = "🚨 HIGH RISK - DRIVER IS DROWSY"

        else:
            result = "❌ Enter valid speed"

    return render_template('index.html', result=result)


# 🔴 CAMERA ROUTE
@app.route('/start_camera')
def start_camera():
    os.system("start cmd /k python drowsiness.py")
    return "Camera Started"


if __name__ == "__main__":
    app.run(debug=True)