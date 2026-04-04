import serial
import time
import threading

class IoTModule:
    def __init__(self, port='COM3', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.is_connected = False
        
        # Sensor Data Simulated as Impact Sensors
        self.ultrasonic_distance = 50.0 # Standard driving distance
        self.impact_sensor_active = 0 # 0=Safe, 1=Crash
        
        self.connect()
        
        if self.is_connected:
            self.read_thread = threading.Thread(target=self._read_serial, daemon=True)
            self.read_thread.start()

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)
            self.is_connected = True
            print(f"Connected to Arduino Crash Sensors on {self.port}")
        except serial.SerialException as e:
            print(f"Warning: Could not connect to Arduino on {self.port}. Running in Simulation Mode.")
            self.is_connected = False

    def _read_serial(self):
        while self.is_connected and self.ser:
            try:
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8').strip()
                    if line.startswith("DIST:"):
                        parts = line.split(',')
                        for part in parts:
                            if "DIST:" in part:
                                self.ultrasonic_distance = float(part.split(':')[1])
                            elif "IMPACT:" in part:
                                self.impact_sensor_active = int(part.split(':')[1])
            except Exception as e:
                pass

    def trigger_crash_alarm(self):
        """Sends command to Arduino to sound crash alarm."""
        print("IoT: Crash Alarm TRIGGERED!")
        if self.is_connected and self.ser:
            self.ser.write(b"ALARM\n")

    def reset_alarm(self):
        """Sends command to Arduino to silence alarm."""
        if self.is_connected and self.ser:
            self.ser.write(b"SAFE\n")

    def get_sensor_data(self):
        """Returns distance and impact status."""
        if not self.is_connected:
            # Simulated data: random smooth fluctuation to simulate driving
            import random
            self.ultrasonic_distance = max(1.0, self.ultrasonic_distance + random.uniform(-5, 5))
            
            # Simulate a 5% chance of severe impact purely for visual dashboard testing
            if random.random() < 0.05:
                self.ultrasonic_distance = 0.5
                self.impact_sensor_active = 1
            else:
                self.impact_sensor_active = 0
            
            # calculate G-force based on distance dropping near 0
            g_force = 100 if self.ultrasonic_distance < 2.0 else 0
            return self.ultrasonic_distance, g_force
            
        return self.ultrasonic_distance, (self.impact_sensor_active * 100) # 100G crash scale
