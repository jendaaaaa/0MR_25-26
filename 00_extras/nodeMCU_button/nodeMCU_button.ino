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