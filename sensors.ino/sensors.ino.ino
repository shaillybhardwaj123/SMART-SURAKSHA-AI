// ============================================================
// SmartSuraksha - Arduino Sensor Code
// Hall Effect Sensor (Speed) + Ultrasonic Sensor (Distance)
// Serial Output Format: DATA,speed,distance
// ============================================================

// ---- Pin Definitions ----
#define HALL_PIN 2
#define TRIG_PIN 9
#define ECHO_PIN 10

// ---- Wheel Config ----
#define WHEEL_DIAMETER_CM 60.0
#define WHEEL_CIRCUMFERENCE_M (3.14159 * WHEEL_DIAMETER_CM / 100.0)
#define MAGNETS_PER_ROTATION 1

// ---- Variables ----
volatile unsigned long pulseCount = 0;
unsigned long lastSpeedCalc = 0;
float speed_kmh = 0.0;
float distance_cm = 0.0;

// ---- Interrupt (IRAM_ATTR removed — not Arduino compatible) ----
void hallPulse() {
    pulseCount++;
}

void setup() {
    Serial.begin(9600);

    pinMode(HALL_PIN, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(HALL_PIN), hallPulse, FALLING);

    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);

    Serial.println("READY");
}

void loop() {
    // ---- Speed Calculation every 1 second ----
    unsigned long now = millis();
    if (now - lastSpeedCalc >= 1000) {

        // Safely copy pulseCount (disable interrupt briefly)
        noInterrupts();
        unsigned long pulses = pulseCount;
        pulseCount = 0;
        interrupts();

        lastSpeedCalc = now;

        float rps     = (float)pulses / MAGNETS_PER_ROTATION;
        float rpm     = rps * 60.0;
        speed_kmh     = (rpm * WHEEL_CIRCUMFERENCE_M * 60.0) / 1000.0;
    }

    // ---- Ultrasonic Distance ----
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    long duration = pulseIn(ECHO_PIN, HIGH, 30000);
    distance_cm = (duration == 0) ? 999.0 : (duration * 0.0343) / 2.0;

    // ---- Send over Serial ----
    Serial.print("DATA,");
    Serial.print(speed_kmh, 1);
    Serial.print(",");
    Serial.println(distance_cm, 1);

    delay(500);
}