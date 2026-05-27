"""
SmartSuraksha - Arduino Bridge (Distance + Relative Speed)
----------------------------------------------------------
Flow:
  Arduino → distance → relative_speed calculate → ML → JSON → Flask → Frontend

relative_speed = (prev_distance - curr_distance) / time_elapsed
Positive = object paas aa raha (dangerous)
Negative = object door ja raha (safe)

Run: python arduino_bridge.py
"""

import serial
import serial.tools.list_ports
import json
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ml_module1 import get_ml_module

BAUD_RATE   = 9600
OUTPUT_FILE = "arduino_data.json"

print("Loading ML model...")
ml = get_ml_module()
print("ML ready!\n")


def find_port():
    ports = serial.tools.list_ports.comports()
    print("Detected Ports:")
    for p in ports:
        print(f"   {p.device} — {p.description}")

    for p in ports:
        desc = p.description.lower()
        if any(x in desc for x in ["arduino", "ch340", "cp210", "usb serial", "uart"]):
            print(f"\nAuto-detected: {p.device}")
            return p.device

    print("\nCould not auto-detect.")
    return input("Enter port (e.g. COM5, COM6): ").strip()


def write_json(data: dict):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f)


def parse_distance(raw: str):
    raw = raw.strip()
    # Format 1: JSON
    if raw.startswith("{"):
        try:
            return float(json.loads(raw).get("distance", 999))
        except:
            pass
    # Format 2: Plain "Distance: 23.4 cm"
    if ":" in raw:
        try:
            part = raw.split(":")[1].strip()
            return float(part.split()[0])
        except:
            pass
    return None


def determine_risk(collision, prob, distance, rel_speed):
    if collision or distance < 15:
        return "HIGH"
    elif prob > 0.5 or (distance < 50 and rel_speed > 20):
        return "HIGH"
    elif prob > 0.25 or distance < 80:
        return "MEDIUM"
    else:
        return "LOW"


def main():
    print("=" * 55)
    print("  SmartSuraksha — Arduino + Relative Speed ML")
    print("=" * 55)

    port = find_port()
    print(f"\nConnecting to {port}...")

    try:
        ser = serial.Serial(port, BAUD_RATE, timeout=2)
        time.sleep(2)
        print("Connected!\n")
    except serial.SerialException as e:
        print(f"\nERROR: {e}")
        print("Fix: Arduino IDE Serial Monitor band karo!")
        input("Press Enter to exit...")
        return

    write_json({
        "status": "connected", "distance": 999, "speed": 0,
        "relative_speed": 0.0, "collision": False,
        "collision_probability": 0.0, "risk": "LOW"
    })

    prev_distance = None
    prev_time     = None

    print(f"{'Dist':>8}  {'Rel.Spd':>10}  {'Prob':>7}  {'Risk':>10}  Collision")
    print("-" * 55)

    while True:
        try:
            raw = ser.readline().decode("utf-8", errors="ignore").strip()
            if not raw:
                continue

            distance = parse_distance(raw)
            if distance is None:
                print(f"[SKIP] {raw}")
                continue

            curr_time = time.time()

            # ── Relative Speed ─────────────────────────────────
            if prev_distance is not None and prev_time is not None:
                elapsed = curr_time - prev_time
                relative_speed = (prev_distance - distance) / elapsed if elapsed > 0 else 0.0
            else:
                relative_speed = 0.0

            prev_distance = distance
            prev_time     = curr_time

            # ── ML Predict ─────────────────────────────────────
            collision, prob = ml.predict_collision(
                distance=distance,
                relative_speed=relative_speed
            )
            risk = determine_risk(collision, prob, distance, relative_speed)

            # ── Write JSON ─────────────────────────────────────
            write_json({
                "status":                "connected",
                "distance":              round(distance, 1),
                "speed":                 0,
                "relative_speed":        round(relative_speed, 1),
                "collision":             collision,
                "collision_probability": prob,
                "risk":                  risk
            })

            # ── Print ──────────────────────────────────────────
            d_s = f"{distance:.1f}cm" if distance < 999 else "---"
            r_s = f"{relative_speed:+.1f}cm/s"
            rsk = {"LOW":"✅ LOW","MEDIUM":"⚡ MED","HIGH":"🔴 HIGH"}.get(risk, risk)
            c_s = "🚨 YES" if collision else "no"
            print(f"{d_s:>8}  {r_s:>10}  {prob*100:>6.0f}%  {rsk:>10}  {c_s}")

        except serial.SerialException:
            print("\nArduino disconnected!")
            write_json({"status":"disconnected","distance":999,"speed":0,
                        "relative_speed":0.0,"collision":False,
                        "collision_probability":0.0,"risk":"LOW"})
            break

        except KeyboardInterrupt:
            print("\nBridge stopped.")
            write_json({"status":"disconnected","distance":999,"speed":0,
                        "relative_speed":0.0,"collision":False,
                        "collision_probability":0.0,"risk":"LOW"})
            break

    ser.close()


if __name__ == "__main__":
    main()