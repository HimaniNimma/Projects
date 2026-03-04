#define trigPin D1   // Connect to GPIO5
#define echoPin D2   // Connect to GPIO4
#define ledPin  D3   // Connect to GPIO0 (built-in LED or external)

// Variables
long duration;
int distance;
bool sent = false;

void setup() {
  Serial.begin(115200);  // Use 115200 for NodeMCU
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // Trigger the ultrasonic sensor
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read the echo
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  // If object is within 10 cm
  if (distance > 0 && distance <= 10 && !sent) {
    Serial.println("A");  // Serial message
    digitalWrite(ledPin, HIGH);                    // Turn LED ON
    delay(2000);
    digitalWrite(ledPin, LOW);                     // Turn LED OFF
    sent = true;
  }

  // Reset the alert flag
  if (distance > 10) {
    sent = false;
  }

  delay(200);
} 

