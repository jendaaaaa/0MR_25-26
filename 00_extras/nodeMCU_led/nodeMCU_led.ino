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

// Define the pin constant
const int BUTTON_PIN = D2; 

void setup() {
  Serial.begin(115200);
  
  // Initialize the internal pull-up resistor
  // This keeps the pin HIGH (1) until the button is pressed (0)
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  Serial.println("Button Test Initialized");
}

void loop() {
  // Read the state of the button
  int buttonState = digitalRead(BUTTON_PIN);

  // Since we use PULLUP, the logic is inverted:
  // LOW (0) means pressed, HIGH (1) means not pressed
  if (buttonState == LOW) {
    Serial.println("Button is PRESSED!");
  }

  delay(50); // Small delay to help with "debounce"
}