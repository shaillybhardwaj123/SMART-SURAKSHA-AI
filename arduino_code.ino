// Smart Traffic Accident Detection Arduino Code
// Constants for pins
const int trigPin = 9;
const int echoPin = 10;
const int impactPin = 2; // Impact switch / Vibration sensor Digital Output
const int sirenPin = 8;
const int warningLed = 13; // Red LED

// Variables
long duration;
float distance;
int impactState;

void setup() {
  Serial.begin(9600); // Initialize Serial Monitor
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(impactPin, INPUT);
  pinMode(sirenPin, OUTPUT);
  pinMode(warningLed, OUTPUT);
  
  digitalWrite(sirenPin, LOW);
  digitalWrite(warningLed, LOW);
}

void loop() {
  // Read distance (e.g., proximity to another car)
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  distance = (duration * 0.0343) / 2; // Distance in cm
  
  // Read Impact Sensor (Assume HIGH means crash)
  impactState = digitalRead(impactPin);
  
  // Send Sensor Data over Serial
  Serial.print("DIST:");
  Serial.print(distance);
  Serial.print(",IMPACT:");
  Serial.println(impactState);
  
  // Listen for AI backend Alarm commands
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove whitespace
    
    if (command == "ALARM") {
      digitalWrite(warningLed, HIGH);
      digitalWrite(sirenPin, HIGH);
    } 
    else if (command == "SAFE") {
       digitalWrite(warningLed, LOW);
       digitalWrite(sirenPin, LOW);
    }
  }
  
  delay(200); // Poll 5 times a second for fast crash response
}
