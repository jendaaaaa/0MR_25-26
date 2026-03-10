void setup() {
  // Initialize serial communication at 115200 bits per second
  Serial.begin(115200);
  delay(1000);
}

void loop() {
  // Send the string to the computer
  Serial.println("Hello from NodeMCU!");
  
  // Wait for 1 second
  delay(1000);
}