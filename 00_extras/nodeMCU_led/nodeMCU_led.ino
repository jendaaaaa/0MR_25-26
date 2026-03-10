void setup() {
  Serial.begin(115200);
  delay(1000);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH); // Start with LED OFF
  Serial.println("Waiting for commands...");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == '1') {
      digitalWrite(LED_BUILTIN, LOW);  // Turn LED ON
      Serial.println("LED is now ON");
    } 
    else if (command == '0') {
      digitalWrite(LED_BUILTIN, HIGH); // Turn LED OFF
      Serial.println("LED is now OFF");
    }
    else if (command != '\n' && command != '\r' ) {
      Serial.println("Unknown command:(((((");
      Serial.println(command);
    }
  }
}